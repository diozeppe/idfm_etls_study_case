import os
import yaml
import pendulum
import pandas as pd
import geopandas as gpd
from utils.helpers import get_engine, extract_json_request, generate_merge_query, get_transform_function
from utils.api_data import insert_api_payload, get_api_payload
from pathlib import Path
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from dotenv import load_dotenv

def create_etl_dag(dag_id, etl_config):
    # ETL config validation
    
    staging_table = "{}_staging".format(etl_config['table_name'])

    def setup():
        hook = PostgresHook(postgres_conn_id = 'idfm_db')

        setup_sql = Path(etl_config["schema_file"]).read_text()

        hook.run(setup_sql)

    def extract():
        data = extract_json_request(etl_config["url"], etl_config['access'])
        insert_api_payload('idfm_db', dag_id, data)

    def transform():
        engine = get_engine('idfm_db')
        transform_fn = get_transform_function(etl_config["transform_fn"]) if "transform_fn" in etl_config else None
        payload = get_api_payload(dag_id, 'idfm_db')
        transform_fn(payload, staging_table, engine)


    def load():
        engine = get_engine('idfm_db')

        hook = PostgresHook(postgres_conn_id = 'idfm_db')

        df = pd.read_sql(f"SELECT * FROM {staging_table}", engine)

        merge_sql = generate_merge_query(df, etl_config["table_name"], staging_table, etl_config["primary_key"])

        hook.run(merge_sql)

    # DAG Definition
    with DAG(
        dag_id = dag_id,
        schedule = etl_config["schedule"],
        start_date = pendulum.datetime(2025, 9, 1, hour=0, tz="UTC"),
        catchup = False,
        tags = ["idfm"],
    ) as dag:
        # Check setup 
        setup = PythonOperator(
            task_id = "setup_{}_dataset".format(etl_config["table_name"]),
            python_callable = setup
        )

        # Extract
        extract = PythonOperator(
            task_id = "extract_{}_dataset".format(etl_config["table_name"]),
            python_callable = extract,
        )

        # Transform
        transform = PythonOperator(
            task_id = "transform_{}_dataset".format(etl_config["table_name"]),
            python_callable = transform
        )

        # Load
        load = PythonOperator(
            task_id = "load_{}_dataset".format(etl_config["table_name"]),
            python_callable = load
        )

        setup >> extract >> transform >> load

    return dag

# Begining of the Dynamic DAG creation
elt_dag_factory_config_path = os.path.dirname(os.path.abspath(__file__)) + "/etl_dag_factory_config.yml"

with open(elt_dag_factory_config_path) as dag_factory_config_file:
    dag_factory_config = yaml.safe_load(dag_factory_config_file)

    for config in dag_factory_config["dags"]:
        dag_id = "idfm_etl_{}".format(config["name"])

        globals()[dag_id] = create_etl_dag(dag_id, config)