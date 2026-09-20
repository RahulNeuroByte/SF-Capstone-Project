USE DATABASE GLOBRORETAIL_DW;
USE SCHEMA OPS;

-- Optional: create an email notification integration first. The integration syntax and
-- recipient allow-list are account-specific, so this procedure only calls it if configured.
CREATE OR REPLACE PROCEDURE SP_REPROCESS_FAILED_FILES()
RETURNS STRING
LANGUAGE JAVASCRIPT
EXECUTE AS OWNER
AS
$$
try {
  var rs = snowflake.createStatement({sqlText:`SELECT FILE_NAME, TABLE_NAME
      FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
        TABLE_NAME=>'GLOBRORETAIL_DW.RAW.RAW_POS_SALES',
        START_TIME=>DATEADD('day',-1,CURRENT_TIMESTAMP())))
      WHERE ERROR_COUNT > 0 LIMIT 20`}).execute();
  var count=0;
  while(rs.next()) {
    var file=rs.getColumnValue(1);
    var target=rs.getColumnValue(2);
    snowflake.createStatement({sqlText:`COPY INTO GLOBRORETAIL_DW.RAW.RAW_POS_SALES
      FROM @GLOBRORETAIL_DW.RAW.STG_POS_SALES FILES=('${file}') FORCE=TRUE
      FILE_FORMAT=(FORMAT_NAME='GLOBRORETAIL_DW.RAW.FF_CSV_STANDARD') ON_ERROR='CONTINUE'`}).execute();
    count++;
  }
  return 'Reprocessed ' + count + ' failed POS files. Extend the procedure for the other three source tables as needed.';
} catch(err) { return 'FAILED: ' + err.message; }
$$;

-- Optional alert procedure. Requires a configured Snowflake notification integration.
CREATE OR REPLACE PROCEDURE SP_SEND_PIPELINE_ALERT(P_SUBJECT STRING, P_BODY STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS OWNER
AS
$$
BEGIN
  -- Uncomment and replace the integration name/recipient after creating the notification integration.
  -- CALL SYSTEM$SEND_EMAIL('GR_EMAIL_INT','your-team@example.com',P_SUBJECT,P_BODY);
  RETURN 'EMAIL_ALERT_TEMPLATE_READY';
EXCEPTION WHEN OTHER THEN
  RETURN 'EMAIL_ALERT_FAILED: ' || SQLERRM;
END;
$$;
