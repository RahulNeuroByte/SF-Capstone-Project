# Upload the supplied CSVs to S3 from Windows PowerShell

Replace `<bucket>` and `<repo-root>` before running.

```powershell
aws s3 mb s3://<bucket>
aws s3 cp .\data_local\pos_sales.csv s3://<bucket>/globo-retail/pos/pos_sales.csv
aws s3 cp .\data_local\online_orders.csv s3://<bucket>/globo-retail/online/online_orders.csv
aws s3 cp .\data_local\product_catalog.csv s3://<bucket>/globo-retail/product/product_catalog.csv
aws s3 cp .\data_local\inventory_device_logs.csv s3://<bucket>/globo-retail/inventory/inventory_device_logs.csv

aws s3 ls s3://<bucket>/globo-retail/ --recursive
```

For the real-time demonstration, upload a second file into one of the same prefixes after the pipes and S3 notifications are active. Snowpipe should process the new object automatically.
