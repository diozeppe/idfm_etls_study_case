import os
import pendulum
from pathlib import Path
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from dotenv import load_dotenv

load_dotenv()

SETUP_SQL_FILE_PATH = os.getenv("SETUP_SQL_FILE_PATH", "")

# Define DAG
with DAG(
    dag_id = "idfm_setup_schema",
    description = "Create inital tables for IDFM ETL APIs",
    start_date = pendulum.datetime(2025, 9, 1, hour=0, tz="UTC"),
    schedule = "@once",
    catchup = False,
    tags = ["idfm", "setup", "schema"]
) as dag:
    sql_file = Path(SETUP_SQL_FILE_PATH).read_text()

    create_setup_schema = SQLExecuteQueryOperator(
        task_id = "create_schema_setup_tables",
        conn_id = 'idfm_db',
        sql = sql_file,
    )

    create_setup_schema
