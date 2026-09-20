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

Do not run the task start script before the required tables, procedures, stages, and pipes exist.

## PowerShell upload example

After configuring AWS CLI and creating the bucket, upload the local files to the required prefixes. Replace the bucket name before running:

```powershell
$bucket = "your-s3-bucket"
aws s3 cp .\data_local\pos_sales.csv "s3://$bucket/globo-retail/pos/"
aws s3 cp .\data_local\online_orders.csv "s3://$bucket/globo-retail/online/"
aws s3 cp .\data_local\product_catalog.csv "s3://$bucket/globo-retail/product/"
aws s3 cp .\data_local\inventory_device_logs.csv "s3://$bucket/globo-retail/inventory/"
```

## Run Snowpark locally

Create a virtual environment and install the pinned dependencies:

```powershell
Set-Location .\09_snowpark
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Set the connection variables for the current PowerShell session. Do not commit real values:

```powershell
$env:SNOWFLAKE_ACCOUNT = "your-account"
$env:SNOWFLAKE_USER = "your-user"
$env:SNOWFLAKE_PASSWORD = "your-password"
$env:SNOWFLAKE_ROLE = "DATA_ENGINEER"
$env:SNOWFLAKE_WAREHOUSE = "GR_TRANSFORM_WH"
$env:SNOWFLAKE_DATABASE = "GLOBRORETAIL_DW"
$env:SNOWFLAKE_SCHEMA = "CORE"
python .\snowpark_pipeline.py
```

For Snowsight, use `09_snowpark/python_worksheet_version.py` in a Python worksheet.

## Validate the deployment

Run `13_tests/01_validation.sql`, then inspect:

- `OPS.PIPELINE_RUN_LOG`
- `OPS.DATA_QUALITY_LOG`
- `SHOW TASKS`
- `SHOW STREAMS`
- `SHOW PIPES`
- `ANALYTICS.DT_DAILY_STORE_REVENUE`
- `ANALYTICS.MV_DAILY_REVENUE`

The expected first load is 1,000 rows per supplied source file. Use the validation SQL as the source of truth if your load timing or reruns produce different counts.

## Security demonstration

The intended demonstration roles are:

| Role | Expected access |
| --- | --- |
| `DATA_ENGINEER` | Unmasked PII and all store regions |
| `DATA_ANALYST` | Masked PII and broad store visibility |
| `DATA_SCIENTIST` | Masked PII and North/South rows |
| `BI_ANALYST` | Masked PII and North-region rows |

Replace placeholder users in the security scripts before granting roles to real users. Never place passwords, private keys, AWS secrets, or account-specific tokens in SQL, Python, or this README.

## GitHub publishing guide

This project is intended to be published under the GitHub account `RahulNeuroByte`.

### Repository details

| Setting | Value |
| --- | --- |
| GitHub owner | `RahulNeuroByte` |
| Recommended repository name | `SF_GloboRetail` |
| HTTPS repository URL | `https://github.com/RahulNeuroByte/SF_GloboRetail.git` |
| Default branch | `main` |
| Recommended visibility | Private until all data and configuration have been reviewed |

The repository should remain empty when it is created on GitHub. Do not ask GitHub to generate another README, `.gitignore`, or license because this project already contains its own files.

### One-time GitHub setup

1. Sign in to GitHub as `RahulNeuroByte`.
2. Open [github.com/new](https://github.com/new).
3. Enter `SF_GloboRetail` as the repository name.
4. Add a short description such as `Snowflake and AWS S3 retail analytics pipeline with Snowpipe, CDC, security, and Snowpark.`
5. Select **Private** for a safe first upload. The repository can be made public later after a complete security review.
6. Leave **Add a README file**, **Add .gitignore**, and **Choose a license** unchecked.
7. Select **Create repository**.

### Review files before the first commit

From PowerShell, open the project folder and review the files Git will stage:

```powershell
Set-Location D:\SF_GloboRetail
git status
Get-ChildItem -Force
```

Before committing, confirm all of the following:

- `config/project.env.example` contains placeholders only.
- No `.env` file, password, private key, AWS access key, Snowflake token, or personal cloud identifier is present.
- `data_local/` contains only approved demonstration data.
- The documentation does not contain confidential account information.
- `docs/` is intentionally included because it contains the project guides.

The repository `.gitignore` excludes common local credentials, virtual environments, logs, and private documentation. GitHub publication is still a human review step; never rely on `.gitignore` as a substitute for checking staged files.

### Initialize and push the project for the first time

Run these commands from `D:\SF_GloboRetail`:

```powershell
Set-Location D:\SF_GloboRetail
git init
git branch -M main
git add .
git status
git diff --cached --check
git commit -m "Initial GloboRetail project"
git remote add origin https://github.com/RahulNeuroByte/SF_GloboRetail.git
git push -u origin main
```

When GitHub asks for HTTPS authentication, use your GitHub username `RahulNeuroByte` and a GitHub personal access token instead of your GitHub account password. A token should be created in GitHub under **Settings -> Developer settings -> Personal access tokens** and should have only the repository permissions required for this upload.

If Git reports that `origin` already exists, inspect it first:

```powershell
git remote -v
```

If the URL is incorrect, replace it with:

```powershell
git remote set-url origin https://github.com/RahulNeuroByte/SF_GloboRetail.git
git push -u origin main
```

### Verify the first upload

Run:

```powershell
git remote -v
git status
git log --oneline -1
git branch --show-current
```

The expected results are:

- The remote points to `RahulNeuroByte/SF_GloboRetail`.
- The current branch is `main`.
- The working tree is clean after the commit.
- The latest commit is `Initial GloboRetail project`.

Then open [github.com/RahulNeuroByte/SF_GloboRetail](https://github.com/RahulNeuroByte/SF_GloboRetail) and confirm that `README.md`, `docs/`, SQL scripts, Python files, configuration templates, and approved local CSV files are visible.

### Future development workflow

Use this sequence whenever the project changes:

```powershell
Set-Location D:\SF_GloboRetail
git pull origin main
git status
git add .
git diff --cached --check
git commit -m "Describe the project change"
git push origin main
```

Use focused commit messages, for example:

- `Add Snowpipe ingestion documentation`
- `Update Snowpark feature pipeline`
- `Improve validation SQL`
- `Document AWS notification setup`

For larger work, create a branch and open a pull request:

```powershell
git switch -c feature/describe-the-change
git add .
git commit -m "Describe the project change"
git push -u origin feature/describe-the-change
```

Review the branch on GitHub, open a pull request into `main`, check the changed files, and merge only after the SQL, Python, documentation, and security review are complete.

### Common GitHub problems

| Problem | Resolution |
| --- | --- |
| `remote origin already exists` | Run `git remote -v`, then use `git remote set-url origin ...` if needed. |
| `rejected because the remote contains work` | The GitHub repository was initialized with files. Pull and reconcile the history, or create a new empty repository. |
| `Authentication failed` | Use a GitHub personal access token for HTTPS or configure SSH authentication. |
| A secret appears in a commit | Revoke or rotate the secret immediately. Removing the file in a later commit is not enough because it remains in Git history. |
| Files are missing from the upload | Run `git status --ignored` and inspect `.gitignore` rules before staging again. |

## Conclusion

GloboRetail provides a complete reference implementation for moving retail data from AWS S3 into Snowflake, processing it through raw, CDC, clean, core, and analytical layers, and exposing governed results for analytics and Snowpark workloads. The numbered folders and documentation make the project repeatable from a clean environment, while the explicit assumptions identify which values must be replaced for a real deployment.

The recommended long-term practice is to keep this GitHub repository free of secrets, update the documentation whenever the execution order changes, validate every pipeline change with `13_tests/01_validation.sql`, and use pull requests for significant improvements. With those controls in place, `RahulNeuroByte/SF_GloboRetail` can serve as a clear portfolio project, a future reference implementation, and a foundation for production-oriented enhancements.
