# Architecture

```text
                       +-----------------------------+
                       |        AWS S3 Bucket        |
                       |  pos / online / product /   |
                       |        inventory            |
                       +--------------+--------------+
                                      |
                         S3 ObjectCreate event
                                      |
                                      v
                       +-----------------------------+
                       | Snowflake Storage Integration|
                       | External Stage + Snowpipe    |
                       +--------------+--------------+
                                      |
                                      v
                       +-----------------------------+
                       |           RAW Layer          |
                       |  RAW_POS_SALES               |
                       |  RAW_ONLINE_ORDERS           |
                       |  RAW_PRODUCT_CATALOG         |
                       |  RAW_INVENTORY_DEVICE_LOGS   |
                       +--------------+--------------+
                                      |
                         Streams / CDC
                                      v
                       +-----------------------------+
                       |          CLEAN Layer         |
                       | cleaned source-aligned data |
                       +--------------+--------------+
                                      |
                             Task DAG + SCD2
                                      v
              +-----------------------+-----------------------+
              |                                               |
              v                                               v
   +------------------------+                    +------------------------+
   |      CORE STAR         |                    |     Snowpark Python    |
   | DIM_CUSTOMER          |                    | DQ / derivations / ML  |
   | DIM_PRODUCT           |                    +------------------------+
   | DIM_STORE             |
   | DIM_DATE              |
   | FACT_SALES            |
   | FACT_INVENTORY        |
   +-----------+------------+
               |
               v
   +-------------------------------+
   | Analytics                     |
   | Dynamic Table                 |
   | Materialized View             |
   | Executive Views / BI          |
   +-------------------------------+
               |
               v
   +-------------------------------+
   | Security                      |
   | RBAC                          |
   | Dynamic Masking               |
   | Row Access Policies           |
   | Secure Views                  |
   +-------------------------------+
```
