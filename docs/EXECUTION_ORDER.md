# Exact File Execution Order

| Order | File | Purpose |
|---:|---|---|
| 1 | `01_setup/00_database.sql` | Database, schemas, warehouses, ops tables |
| 2 | `01_setup/01_file_formats.sql` | CSV formats |
| 3 | `03_raw/01_raw_tables.sql` | Raw ingestion tables |
| 4 | `04_cdc/01_streams.sql` | CDC streams |
| 5 | `04_cdc/02_clean_tables.sql` | Clean layer |
| 6 | `05_transform/01_core_tables.sql` | Star schema + inventory/features |
| 7 | `02_ingestion/01_storage_integration.sql` | AWS trust integration |
| 8 | `02_ingestion/02_stages.sql` | S3 external stages |
| 9 | `02_ingestion/03_pipes.sql` | Snowpipes |
| 10 | AWS console | S3 notifications to Snowpipe SQS |
| 11 | Windows PowerShell | Upload supplied CSVs |
| 12 | `05_transform/02_date_store_seed.sql` | Date/store dimensions |
| 13 | `07_procedures/01_stored_procedures.sql` | SCD2, DQ, analytics procedures |
| 14 | `07_procedures/02_reprocess_and_alerts.sql` | Reprocessing/alert templates |
| 15 | `10_analytics/01_dynamic_table_and_views.sql` | Dynamic table, MV, executive view |
| 16 | `06_security/01_roles_and_grants.sql` | RBAC |
| 17 | `06_security/02_policies.sql` | Masking, row access, secure views |
| 18 | `08_tasks/01_task_dag.sql` | Task DAG creation |
| 19 | `08_tasks/99_start_pipeline.sql` | Start and demo-run DAG |
| 20 | `13_tests/01_validation.sql` | Functional validation |
| 21 | `09_snowpark/snowpark_pipeline.py` | Snowpark transformations/features |
| 22 | `11_performance/01_optimization.sql` | Clustering, concurrency, resource monitor |
| 23 | `11_performance/02_query_history.sql` | Performance report |
| 24 | `11_performance/03_time_travel.sql` | Recovery demo |
