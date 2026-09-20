# SETUP_STEPS.md — Complete Execution Order

## Phase 0 — Prerequisites

### Snowflake
- Snowflake account with permissions to create databases, warehouses, integrations, roles, policies, tasks and stages.
- Enterprise Edition or higher is required for Dynamic Data Masking and Row Access Policies.
- A Snowflake warehouse such as `GR_WH`.

### AWS
- AWS account.
- S3 bucket.
- IAM permission to create an IAM policy and role.
- AWS CLI installed if you want PowerShell uploads.

### Local Python
- Python 3.11+ recommended.
- Install `09_snowpark/requirements.txt` only if local Snowpark execution is required.

## Phase 1 — Create Snowflake foundation

Run:
1. `01_setup/00_database.sql`
2. `01_setup/01_file_formats.sql`
3. `03_raw/01_raw_tables.sql`
4. `04_cdc/01_streams.sql`
5. `04_cdc/02_clean_tables.sql`
6. `05_transform/01_core_tables.sql`

Do not start the task DAG yet.

## Phase 2 — Configure AWS S3 + IAM

1. Create an S3 bucket.
2. Create an IAM policy from `02_ingestion/aws_iam_policy.json`.
3. Create an IAM role using `02_ingestion/aws_trust_policy.template.json`.
4. In Snowflake run `02_ingestion/01_storage_integration.sql` after replacing the role ARN and bucket.
5. Run `DESC STORAGE INTEGRATION GR_S3_INT`.
6. Copy `STORAGE_AWS_IAM_USER_ARN` and `STORAGE_AWS_EXTERNAL_ID` into the AWS role trust relationship.


7. Run `02_ingestion/02_stages.sql` after replacing `<S3_BUCKET>`.
8. Run `02_ingestion/03_pipes.sql`.
9. Run `SHOW PIPES` and save the `notification_channel` SQS ARN for each pipe.
10. Configure S3 ObjectCreate notifications to the Snowflake SQS queue(s), following `02_ingestion/S3_UPLOAD_WINDOWS.md` and the official Snowflake procedure.

## Phase 3 — Upload the supplied data

Upload exactly the supplied CSV files:
- `pos_sales.csv` -> `globo-retail/pos/`
- `online_orders.csv` -> `globo-retail/online/`
- `product_catalog.csv` -> `globo-retail/product/`
- `inventory_device_logs.csv` -> `globo-retail/inventory/`

Verify:
`LIST @RAW.STG_POS_SALES;`
`SELECT COUNT(*) FROM RAW.RAW_POS_SALES;`

Expected first-load counts are 1,000 rows for each supplied file.

## Phase 4 — Seed dimensions

After the raw files have landed, run:
`05_transform/02_date_store_seed.sql`

This creates the 100 store records represented by the source IDs and a 2024 date dimension. Store attributes are deterministic demo enrichment because the source does not provide city/state.

## Phase 5 — Deploy procedures

Run:
1. `07_procedures/01_stored_procedures.sql`
2. `07_procedures/02_reprocess_and_alerts.sql`

Validate with:
`CALL OPS.SP_RUN_DATA_QUALITY();`

## Phase 6 — Deploy analytics

Run:
`10_analytics/01_dynamic_table_and_views.sql`

The dynamic table has a 10-minute target lag and can also be manually refreshed.

## Phase 7 — Deploy security

Run:
1. `06_security/01_roles_and_grants.sql`
2. `06_security/02_policies.sql`

Assign roles to real users only after replacing the placeholder user names.

## Phase 8 — Deploy task DAG

Run:
`08_tasks/01_task_dag.sql`

The tasks remain suspended.

Then run:
`08_tasks/99_start_pipeline.sql`

This enables the DAG and executes the root task for the demo.

## Phase 9 — Validate the pipeline

Run:
`13_tests/01_validation.sql`

Also inspect:
- `OPS.PIPELINE_RUN_LOG`
- `OPS.DATA_QUALITY_LOG`
- `SHOW TASKS`
- `SHOW STREAMS`
- `SHOW PIPES`
- `ANALYTICS.DT_DAILY_STORE_REVENUE`
- `ANALYTICS.MV_DAILY_REVENUE`

## Phase 10 — Snowpark

For local execution:

```powershell
cd .\09_snowpark
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SNOWFLAKE_ACCOUNT="<account>"
$env:SNOWFLAKE_USER="<user>"
$env:SNOWFLAKE_PASSWORD="<password>"
$env:SNOWFLAKE_ROLE="DATA_ENGINEER"
$env:SNOWFLAKE_WAREHOUSE="GR_TRANSFORM_WH"
$env:SNOWFLAKE_DATABASE="GLOBRORETAIL_DW"
$env:SNOWFLAKE_SCHEMA="CORE"
python .\snowpark_pipeline.py
```

For Snowsight, use `09_snowpark/python_worksheet_version.py` in a Python worksheet.

## Phase 11 — Performance demonstration

Run `11_performance/01_optimization.sql` and `11_performance/02_query_history.sql`.

Capture:
- elapsed time
- bytes scanned
- partitions scanned
- partitions total
- pruning percentage
- warehouse credits

Because the supplied demonstration dataset contains only 2,000 sales rows, a dramatic clustering benefit should NOT be claimed. Demonstrate the mechanism and explain that production-scale gains require larger volumes.

## Phase 12 — Security demonstration

### DATA_ENGINEER
Should see unmasked PII and all store regions.

### DATA_ANALYST
Should see masked PII but broad store visibility.

### DATA_SCIENTIST
Should see masked PII and only North/South store rows.

### BI_ANALYST
Should see masked PII and only North-region store rows.

Use `POLICY_CONTEXT` or switch roles in Snowsight to demonstrate the policies safely.

## Phase 13 — Time Travel

Run `11_performance/03_time_travel.sql` and explain that recovery is based on Snowflake Time Travel rather than an external backup copy.

## Phase 14 — Final demonstration order

1. Show source CSVs.
2. Show AWS S3 prefixes.
3. Show external stage.
4. Show Snowpipe.
5. Upload a new CSV object and show auto-ingestion.
6. Show stream records before/after task consumption.
7. Show cleaned tables.
8. Show SCD2 dimension.
9. Show fact sales.
10. Show task DAG.
11. Show dynamic table and materialized view.
12. Switch roles and demonstrate masking/row access.
13. Show Snowpark features.
14. Show query history/performance.
15. Show Time Travel recovery.
16. End with business KPIs.

## Edition/feature note

Dynamic Data Masking and Row Access Policies are Enterprise Edition (or higher) features. If your account does not have them, the security SQL will fail at policy creation/application; use a supported Snowflake edition for the full capstone demonstration.
