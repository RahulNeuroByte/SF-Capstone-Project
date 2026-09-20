# Data Model

## Required star-schema objects from the supplied SQL

- `DIM_CUSTOMER(CUSTOMER_KEY, CUSTOMER_ID, CUSTOMER_NAME, CUSTOMER_SEGMENT, COUNTRY)`
- `DIM_PRODUCT(PRODUCT_KEY, PRODUCT_ID, PRODUCT_NAME, CATEGORY, PRICE)`
- `DIM_STORE(STORE_KEY, STORE_ID, STORE_NAME, CITY, STATE)`
- `DIM_DATE(DATE_KEY, FULL_DATE, YEAR, MONTH, DAY)`
- `FACT_SALES(SALES_KEY, CUSTOMER_KEY, PRODUCT_KEY, STORE_KEY, DATE_KEY, SALES_AMOUNT)`

## Extended production-demo columns

The implementation adds:
- SCD2 effective dates and current flags.
- Product status/history.
- Synthetic PII fields required by the security requirement.
- Revenue/tax/discount metrics.
- Source type and source transaction ID.
- Transaction and ingestion timestamps.
- Inventory fact support.
- Snowpark ML feature table.

## Source-to-model mapping

| Source | Core target | Mapping |
|---|---|---|
| `pos_sales.csv` | `FACT_SALES` | SALE_ID, CUSTOMER_ID, PRODUCT_ID, STORE_ID, SALE_AMOUNT |
| `online_orders.csv` | `FACT_SALES` | ORDER_ID, CUSTOMER_ID, PRODUCT_ID, ORDER_DATE, ORDER_AMOUNT |
| `product_catalog.csv` | `DIM_PRODUCT` | PRODUCT_ID, PRODUCT_NAME, CATEGORY, PRICE, STATUS |
| `inventory_device_logs.csv` | `FACT_INVENTORY` + store support | DEVICE_ID, STORE_ID, PRODUCT_ID, QUANTITY_ON_HAND, LOG_TIMESTAMP |
| derived calendar | `DIM_DATE` | 2024 calendar |

## Cardinality observed in the supplied files

- POS: 1,000 rows, 617 distinct customers, 635 distinct products, 100 stores.
- Online: 1,000 rows, 623 distinct customers, 618 distinct products.
- Product catalog: 1,000 products, 4 categories, 2 statuses.
- Inventory: 1,000 rows, 1,000 devices, 100 stores, 629 distinct products.
- All supplied files are null-free and contain no duplicate full rows.
