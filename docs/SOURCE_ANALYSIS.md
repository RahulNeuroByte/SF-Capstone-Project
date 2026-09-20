# Supplied Source Analysis

| File | Rows | Columns | Null cells | Duplicate full rows |
|---|---:|---:|---:|---:|
| pos_sales.csv | 1,000 | 5 | 0 | 0 |
| online_orders.csv | 1,000 | 5 | 0 | 0 |
| product_catalog.csv | 1,000 | 5 | 0 | 0 |
| inventory_device_logs.csv | 1,000 | 5 | 0 | 0 |

## Cross-source checks

- All POS product IDs exist in product catalog.
- All online product IDs exist in product catalog.
- All inventory product IDs exist in product catalog.
- POS and inventory both use 100 stores.
- POS and online customer IDs overlap for 386 customers.

## Key ranges

- POS sale amount: 10.55–499.68.
- Online order amount: 20.56–799.08.
- Product price: 5.53–997.67.
- Inventory quantity: 0–500.
- Online and inventory dates: 2024-01-01 to 2024-12-30.
