"""Snowpark Python pipeline for GloboRetail.
Run locally with a Snowflake connection, or adapt the main() function to a Python worksheet.
"""
import os
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, coalesce, lit, when, avg, stddev, count, sum as sf_sum, lag, row_number
from snowflake.snowpark.window import Window


def build_session():
    return Session.builder.configs({
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "role": os.getenv("SNOWFLAKE_ROLE", "DATA_ENGINEER"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "GR_TRANSFORM_WH"),
        "database": os.getenv("SNOWFLAKE_DATABASE", "GLOBRORETAIL_DW"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA", "CORE"),
    }).create()


def transform_inventory(session):
    df = session.table("GLOBRORETAIL_DW.CORE.FACT_INVENTORY")
    cleaned = (
        df.with_column("QUANTITY_ON_HAND", coalesce(col("QUANTITY_ON_HAND"), lit(0)))
          .with_column("LOW_STOCK_FLAG", when(col("QUANTITY_ON_HAND") < lit(20), lit(1)).otherwise(lit(0)))
    )
    cleaned.write.mode("overwrite").save_as_table("GLOBRORETAIL_DW.CORE.FACT_INVENTORY_SNOWPARK")
    return cleaned


def build_features(session):
    fact = session.table("GLOBRORETAIL_DW.CORE.FACT_SALES")
    store = session.table("GLOBRORETAIL_DW.CORE.DIM_STORE")

    base = (
        fact.join(store, fact["STORE_KEY"] == store["STORE_KEY"], "left")
            .group_by(fact["TRANSACTION_DATE"], fact["STORE_KEY"], store["STORE_ID"])
            .agg(
                sf_sum(fact["REVENUE_AMOUNT"]).alias("TOTAL_REVENUE"),
                count(lit(1)).alias("TRANSACTION_COUNT"),
                avg(fact["REVENUE_AMOUNT"]).alias("AVG_TRANSACTION_VALUE"),
            )
    )

    w = Window.partition_by(col("STORE_KEY")).order_by(col("TRANSACTION_DATE"))
    stats_w = Window.partition_by(col("STORE_KEY"))
    features = (
        base.with_column("REVENUE_LAG_1_DAY", lag(col("TOTAL_REVENUE"), 1).over(w))
            .with_column("REVENUE_MEAN", avg(col("TOTAL_REVENUE")).over(stats_w))
            .with_column("REVENUE_STDDEV", stddev(col("TOTAL_REVENUE")).over(stats_w))
            .with_column(
                "ANOMALY_SCORE",
                when(col("REVENUE_STDDEV") == 0, lit(0))
                .otherwise((col("TOTAL_REVENUE") - col("REVENUE_MEAN")) / col("REVENUE_STDDEV"))
            )
            .select("TRANSACTION_DATE", "STORE_KEY", "STORE_ID", "TOTAL_REVENUE",
                    "TRANSACTION_COUNT", "AVG_TRANSACTION_VALUE", "REVENUE_LAG_1_DAY",
                    "ANOMALY_SCORE")
    )
    features.write.mode("overwrite").save_as_table("GLOBRORETAIL_DW.CORE.ML_FEATURES_SNOWPARK")
    return features


def run_quality_checks(session):
    checks = {}
    checks["negative_sales"] = session.sql(
        "SELECT COUNT(*) FROM GLOBRORETAIL_DW.CORE.FACT_SALES WHERE SALES_AMOUNT < 0"
    ).collect()[0][0]
    checks["null_revenue"] = session.sql(
        "SELECT COUNT(*) FROM GLOBRORETAIL_DW.CORE.FACT_SALES WHERE REVENUE_AMOUNT IS NULL"
    ).collect()[0][0]
    checks["null_product_keys"] = session.sql(
        "SELECT COUNT(*) FROM GLOBRORETAIL_DW.CORE.FACT_SALES WHERE PRODUCT_KEY IS NULL"
    ).collect()[0][0]
    return checks


def main():
    session = build_session()
    try:
        transform_inventory(session)
        features = build_features(session)
        checks = run_quality_checks(session)
        print("Snowpark pipeline completed")
        print("DQ:", checks)
        features.show(20)
    finally:
        session.close()


if __name__ == "__main__":
    main()
