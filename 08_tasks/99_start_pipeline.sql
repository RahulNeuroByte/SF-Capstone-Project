USE DATABASE GLOBRORETAIL_DW;
USE SCHEMA OPS;

ALTER TASK TASK_05_DATA_QUALITY RESUME;
ALTER TASK TASK_04_REFRESH_ANALYTICS RESUME;
ALTER TASK TASK_03_LOAD_FACTS RESUME;
ALTER TASK TASK_02_SCD2_DIMENSIONS RESUME;
ALTER TASK TASK_01_RAW_TO_CLEAN RESUME;

-- Manual first run. The root task is event-triggered, so after enabling it, new stream data
-- will trigger the graph. For an immediate demo, execute the root task manually:
EXECUTE TASK TASK_01_RAW_TO_CLEAN;
