# 15-Minute Project Demonstration Script

## 1. Business opening — 60 sec

“GloboRetail receives POS, online, product and IoT inventory data. The target architecture removes batch-only processing and creates continuous Snowflake analytics with governance.”

## 2. Source evidence — 60 sec

Show the four supplied CSV files and explain their exact columns. Mention the source has 1,000 records per file.

## 3. AWS ingestion — 90 sec

Show the S3 bucket prefixes, Snowflake storage integration, external stages and four Snowpipes. Explain that S3 ObjectCreate events trigger Snowpipe through the AWS notification path.

## 4. Raw + CDC — 90 sec

Show raw tables and streams. Explain `METADATA$ACTION` and `METADATA$ISUPDATE`.

## 5. Task DAG — 90 sec

Open the task graph. Explain:
`TASK_01_RAW_TO_CLEAN -> TASK_02_SCD2_DIMENSIONS -> TASK_03_LOAD_FACTS -> TASK_04_REFRESH_ANALYTICS -> TASK_05_DATA_QUALITY`.

## 6. Star schema — 90 sec

Show DIM_CUSTOMER, DIM_PRODUCT, DIM_STORE, DIM_DATE and FACT_SALES. Explain surrogate keys and source transaction IDs.

## 7. Security — 120 sec

Switch between roles and query `SECURITY.SECURE_V_CUSTOMER` and `SECURITY.SECURE_V_STORE_SALES`. Demonstrate masked PII and region filtering.

## 8. Snowpark — 90 sec

Run the Snowpark pipeline and show feature columns, null handling, low-stock flagging and anomaly score.

## 9. Performance — 90 sec

Show the clustering key, query history view, partitions scanned/total and warehouse auto-suspend. Explain that 4,000 source rows are too small to claim production-scale speedups.

## 10. Recovery — 60 sec

Show the Time Travel query and recovery clone.

## 11. Closing — 60 sec

Summarize continuous ingestion, CDC, orchestration, SCD2, star schema, Snowpark, security, optimization and recovery.
