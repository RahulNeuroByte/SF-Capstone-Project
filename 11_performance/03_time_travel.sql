USE DATABASE GLOBRORETAIL_DW;
USE SCHEMA CORE;

-- Demonstration: inspect the table as it existed 5 minutes earlier.
SELECT COUNT(*) AS HISTORICAL_ROW_COUNT
FROM FACT_SALES AT (OFFSET => -60*5);

-- Recovery pattern: clone the historical state into a recovery table.
CREATE OR REPLACE TABLE FACT_SALES_RECOVERY
CLONE FACT_SALES AT (OFFSET => -60*5);

SELECT COUNT(*) FROM FACT_SALES_RECOVERY;
