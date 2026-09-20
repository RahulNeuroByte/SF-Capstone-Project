# Known Limitations and Environment-Specific Values

The implementation is complete at the code/design level. The following values cannot be hardcoded because they belong to the user's AWS/Snowflake environment:

- Snowflake account identifier
- Snowflake username/password or key-pair
- AWS account ID
- S3 bucket name and region
- AWS IAM role ARN
- Snowflake-generated IAM user ARN
- Snowflake-generated external ID
- Snowpipe SQS notification channel ARN
- real Snowflake user names for role assignment
- optional email notification integration and recipient allow-list

These are configuration values, not missing project logic.

## Source-driven limitations

The supplied files do not contain:
- POS transaction dates
- customer PII
- customer descriptive attributes
- store descriptive attributes
- discount rates
- tax rates
- payment card data

The project therefore uses deterministic demo enrichments and explicitly documents them. They are placeholders for a production master-data source, not invented business facts.

## Scale limitation

The supplied files total only 4,000 source rows. Clustering, multi-cluster concurrency and cost-management demonstrations are architecturally implemented, but performance results from this small dataset should not be extrapolated to the stated multinational production workload.
