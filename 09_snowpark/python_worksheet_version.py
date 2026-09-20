import snowflake.snowpark as snowpark
from snowflake.snowpark.functions import col, coalesce, lit, when, avg, stddev, count, sum as sf_sum, lag
from snowflake.snowpark.window import Window


def main(session: snowpark.Session):
    fact = session.table("GLOBRORETAIL_DW.CORE.FACT_SALES")
    store = session.table("GLOBRORETAIL_DW.CORE.DIM_STORE")
    df = (fact.join(store, fact["STORE_KEY"] == store["STORE_KEY"], "left")
             .group_by(fact["TRANSACTION_DATE"], fact["STORE_KEY"], store["STORE_ID"])
             .agg(sf_sum(fact["REVENUE_AMOUNT"]).alias("TOTAL_REVENUE"),
                  count(lit(1)).alias("TRANSACTION_COUNT"),
                  avg(fact["REVENUE_AMOUNT"]).alias("AVG_TRANSACTION_VALUE")))
    w = Window.partition_by(col("STORE_KEY")).order_by(col("TRANSACTION_DATE"))
    stats = Window.partition_by(col("STORE_KEY"))
    result = (df.with_column("REVENUE_LAG_1_DAY", lag(col("TOTAL_REVENUE")).over(w))
                .with_column("MEAN_REVENUE", avg(col("TOTAL_REVENUE")).over(stats))
                .with_column("STDDEV_REVENUE", stddev(col("TOTAL_REVENUE")).over(stats))
                .with_column("ANOMALY_SCORE",
                    when(col("STDDEV_REVENUE") == 0, lit(0))
                    .otherwise((col("TOTAL_REVENUE")-col("MEAN_REVENUE"))/col("STDDEV_REVENUE"))))
    return result
