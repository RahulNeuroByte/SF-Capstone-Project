# GloboRetail - Real-Time Retail Sales Analytics Platform

GloboRetail is an end-to-end retail analytics capstone built with Snowflake, AWS S3, Snowpipe, Snowpark, and SQL. It demonstrates cloud ingestion, CDC, data quality, SCD Type 2 dimensions, a star schema, role-based security, analytics objects, task orchestration, performance checks, and Time Travel recovery.

This repository is a reproducible project template. Cloud identifiers, user names, notification channels, and credentials remain as placeholders and must be supplied in your own environment.

## What the project demonstrates

- Batch and event-driven ingestion from AWS S3 into Snowflake.
- Snowpipe auto-ingestion into RAW tables.
- Streams for change data capture and CLEAN tables for standardized data.
- SCD Type 2 processing for customer and product dimensions.
- A retail star schema with `DIM_CUSTOMER`, `DIM_PRODUCT`, `DIM_STORE`, `DIM_DATE`, and `FACT_SALES`.
- Data quality checks, pipeline run logging, and reprocessing procedures.
- Snowflake tasks that coordinate the transformation pipeline.
- Dynamic tables, materialized views, and executive reporting views.
- Role-based access, dynamic masking, row access policies, and secure views.
- Snowpark feature generation for downstream analytics or machine learning.
- Query history, clustering, warehouse, and Time Travel demonstrations.

## Architecture

```text
AWS S3
	-> Snowflake external stages
	-> Snowpipe
	-> RAW tables
	-> Streams
	-> CLEAN tables
	-> SCD2 and core dimensions
	-> FACT_SALES
	-> Dynamic table and materialized view
	-> Secure views and BI access
	-> Snowpark features
```

## Source data

The supplied local data contains four CSV files, each with 1,000 demonstration rows:

| File | Main columns | Destination |
| --- | --- | --- |
| `data_local/pos_sales.csv` | `sale_id, customer_id, product_id, store_id, sale_amount` | `RAW.RAW_POS_SALES` |
| `data_local/online_orders.csv` | `order_id, customer_id, product_id, order_date, order_amount` | `RAW.RAW_ONLINE_ORDERS` |
| `data_local/product_catalog.csv` | `product_id, product_name, category, price, status` | `RAW.RAW_PRODUCT_CATALOG` |
| `data_local/inventory_device_logs.csv` | `device_id, store_id, product_id, quantity_on_hand, log_timestamp` | `RAW.RAW_INVENTORY_DEVICE_LOGS` |

## Important demo assumptions

1. POS sales has no transaction date, so `LOADED_AT` is used as the POS `TRANSACTION_DATE` proxy. Online orders use the source `ORDER_DATE`.
2. The source files do not contain customer PII, customer attributes, or store location attributes. Deterministic synthetic enrichment is generated only to demonstrate the target schema and security policies. It is not real customer data.
3. The source files do not contain discount or tax fields. The demonstration uses `OPS.PIPELINE_PARAMETERS` with 0% discount and 18% tax. Replace these values with approved production rules.
4. Dynamic masking and row access policies require Snowflake Enterprise Edition or higher.
5. The demonstration dataset is intentionally small. Performance results should explain the mechanism, not claim production-scale improvements.

## Repository layout

| Directory | Purpose |
| --- | --- |
| `00_reference/` | Supplied star-schema reference files |
| `01_setup/` | Database, schema, warehouse, and file format setup |
| `02_ingestion/` | AWS integration, stages, pipes, IAM templates, and upload guidance |
| `03_raw/` | Raw landing tables |
| `04_cdc/` | Streams and clean tables |
| `05_transform/` | Core tables, seeds, merges, and fact loading |
| `06_security/` | Roles, grants, masking, row access, and secure views |
| `07_procedures/` | Stored procedures, quality checks, and reprocessing |
| `08_tasks/` | Task DAG and pipeline start script |
| `09_snowpark/` | Local and Snowsight Snowpark implementations |
| `10_analytics/` | Dynamic tables, materialized views, and reporting views |
| `11_performance/` | Optimization, query history, and Time Travel demos |
| `13_tests/` | Validation SQL |
| `config/` | Safe environment-variable template |
| `data_local/` | Supplied demonstration CSV files |
| `docs/` | Architecture, setup, execution, connection, and limitation guides |
| `config/report/` | Project report assets |

## Prerequisites

- A Snowflake account with permission to create databases, warehouses, stages, integrations, pipes, tasks, roles, policies, and tables.
- Snowflake Enterprise Edition or higher for the complete security demonstration.
- An AWS account and S3 bucket.
- Permission to create or configure the AWS IAM policy and role used by the Snowflake storage integration.
- AWS CLI if you want to upload files from PowerShell.
- Python 3.11 or later for local Snowpark execution.
- Git and a GitHub account.

## Run the Snowflake project

1. Run `01_setup/00_database.sql` and `01_setup/01_file_formats.sql`.
2. Create raw, CDC, clean, and core objects using the files in `03_raw/`, `04_cdc/`, and `05_transform/`.
3. Create the AWS S3 bucket, IAM policy, IAM role, and Snowflake storage integration.
4. Replace `<S3_BUCKET>` and other environment placeholders in the ingestion SQL, then create stages and pipes.
5. Configure S3 ObjectCreate notifications for the Snowpipe notification channels.
6. Upload the four files from `data_local/` to the prefixes described in `docs/SETUP_STEPS.md`.
7. Run the date/store seed and stored procedure scripts.
8. Deploy analytics objects, security objects, and the task DAG.
9. Start the pipeline with `08_tasks/99_start_pipeline.sql`.
10. Run `13_tests/01_validation.sql` and inspect the run logs, task status, pipe status, and analytics objects.

## Security demonstration

The intended demonstration roles are:

| Role | Expected access |
| --- | --- |
| `DATA_ENGINEER` | Unmasked PII and all store regions |
| `DATA_ANALYST` | Masked PII and broad store visibility |
| `DATA_SCIENTIST` | Masked PII and North/South rows |
| `BI_ANALYST` | Masked PII and North-region rows |

## Conclusion

SF-Capstone-Project provides a complete reference implementation for moving retail data from AWS S3 into Snowflake, processing it through raw, CDC, clean, core, and analytical layers, and exposing governed results for analytics and Snowpark workloads. The numbered folders and documentation make the project repeatable from a clean environment, while the explicit assumptions identify which values must be replaced for a real deployment.

The recommended long-term practice is to keep this GitHub repository free of secrets, update the documentation whenever the execution order changes, validate every pipeline change with `13_tests/01_validation.sql`, and use pull requests for significant improvements. With those controls in place, `RahulNeuroByte/SF-Capstone-Project` can serve as a clear portfolio project, a future reference implementation, and a foundation for production-oriented enhancements.
