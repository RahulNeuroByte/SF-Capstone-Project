# Connection Steps

## Snowflake -> AWS S3

1. Create the S3 bucket.
2. Create the AWS read policy from `02_ingestion/aws_iam_policy.json`.
3. Create the IAM role.
4. Run `DESC STORAGE INTEGRATION GR_S3_INT` in Snowflake.
5. Put the returned Snowflake IAM user ARN and external ID into `aws_trust_policy.template.json`.
6. Update the trust relationship of the AWS role.
7. Verify the role ARN is the same one referenced by `GR_S3_INT`.
8. Run `LIST @RAW.STG_POS_SALES` and verify the bucket can be listed.

## S3 -> Snowpipe

1. Run `SHOW PIPES`.
2. Copy the Snowflake notification channel/SQS ARN.
3. Open the S3 bucket's Event Notifications.
4. Configure ObjectCreate events for the four prefixes.
5. Target the Snowflake SQS notification channel.
6. Upload a test file.
7. Check `SELECT COUNT(*)` in the corresponding RAW table.
8. Check pipe status and load history.

## Python -> Snowflake

Set the environment variables shown in `config/project.env.example`.
Do not put credentials in source code.

## BI tool -> Snowflake

Use the `BI_ANALYST` role and connect to:
- `GLOBRORETAIL_DW.SECURITY.SECURE_V_STORE_SALES`
- `GLOBRORETAIL_DW.ANALYTICS.V_EXECUTIVE_SALES`

For a real BI connection, use a dedicated BI service user with only the required role and warehouse privileges.
