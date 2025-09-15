import json
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime

def insert_api_payload(conn_id, source, data):
    hook = PostgresHook(postgres_conn_id = conn_id)

    insert_sql = """
        INSERT INTO api_data (source_name, run_date, payload)
        VALUES (%s, %s, %s);
    """

    hook.run(insert_sql, parameters=(source, datetime.today().date(), json.dumps(data)))


def get_api_payload(source: str, conn_id: str):
    hook = PostgresHook(postgres_conn_id = conn_id)

    sql = """
        SELECT payload
        FROM api_data
        WHERE source_name = %s
        ORDER BY run_date DESC
        LIMIT 1
    """

    record = hook.get_first(sql, parameters=(source,))

    if not record:
        raise ValueError(f"No records found for source '{source}'")

    return record[0]