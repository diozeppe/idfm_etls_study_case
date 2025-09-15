import os
import requests
import importlib
import pandas as pd
from airflow.hooks.base import BaseHook
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def get_engine(conn_id: str):
    conn = BaseHook.get_connection(conn_id)
    uri = conn.get_uri()

    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql+psycopg2://", 1)

    return create_engine(uri)

# Fetch dataset from IDFM API and return DataFrame
def extract_json_request(url: str, access: str):
    headers = {}

    if (access == 'apiKey'):
        headers['apiKey'] = os.getenv("IDFM_API_KEY", "")
        
    resp = requests.get(url, headers=headers)

    resp.raise_for_status()

    return resp.json()

def generate_merge_query(df: pd.DataFrame, table_name: str, staging_table: str, primary_key: str = "id"):
    return f"""
        MERGE INTO {table_name} AS target
        USING {staging_table} AS source
        ON target.{primary_key} = source.{primary_key}
        WHEN MATCHED THEN
            UPDATE SET {', '.join([f"{col} = source.{col}" for col in df.columns if col != primary_key])}
        WHEN NOT MATCHED THEN
            INSERT ({', '.join(df.columns)})
            VALUES ({', '.join([f"source.{col}" for col in df.columns])});
    """

# Load Transformation function for the dataset
def get_transform_function(module_path: str):
    module = importlib.import_module(module_path)
    
    return getattr(module, "transform", None)

