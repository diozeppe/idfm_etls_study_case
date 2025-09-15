## About this project

This is a study casy on a simple ETL process, orchestrated by Airflow and using IDFM public data from the Île-de-France mobility network.

At this initial stage, it'll import some of the datasets of the network (Stops, Lines, Routes, and Operators) as well as disruption information.

The objective is to store disruption information over time and create data warehouses, data marts, and similar systems, in order to analyze disruption patterns and identify internal and external correlations.

## Stack used
- Docker
- [Apache Airflow (3.0.6)](https://hub.docker.com/r/apache/airflow)
- Python (3.12)
- [Pandas](https://pandas.pydata.org) and [GeoPandas](https://geopandas.org/en/stable/) (It'll be moved to PySpark in the future)
- PostgreSQL with PostGIS extension

---

## How it works?

1. **Config-driven**  
   - The YAML file in `etl_dag_factory_config.yml` define datasets (name, URL, primary key, transform function path, schema file, schedule). The DAG factory reads the YAML and instantiates DAGs with the given schedule and tasks.

2. **Ingest task**  
   - Fetch latest JSON from the remote API.
   - Persist raw response to a `api_data` table (payload, run_date, source_name) for lineage.

3. **Transform task**  
   - Load raw payload into a Pandas DataFrame.
   - Use modular functions and `.pipe()` to compose the pipeline.

4. **Staging & Load**  
   - Write DataFrame into a staging table using SQLAlchemy `to_sql`. Use `dtype` to ensure columns that must be `JSONB` or `TEXT[]` are created with correct Postgres types.
   - Perform a `MERGE` (or `INSERT ... ON CONFLICT`) from staging into target, casting types as needed.

---

## Run locally 

1. Create your account at [PRIM](https://prim.iledefrance-mobilites.fr) to have access to your API KEY

2. Clone
   
```bash
git clone https://github.com/diozeppe/idfm_etls_study_case.git
cd idfm_etls_study_case/airflow
```

3. Create a `.env` file using the `.env.exemple` as base

```bash
cat .env.exemple >> .env
```

4. Set your `.env` variables

- `IDFM_API_KEY`: from your PRIM account 
- `AIRFLOW_UID`: your current user user id
```bash
id -u
```
- `AIRFLOW__CORE__FERNET_KEY` generated with:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())
```
- `AIRFLOW__API_AUTH__JWT_SECRET` generated with:
```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

5. Run Docker compose

```bash
sudo docker compose up
```

6. If your run was successful, access the AirflowUI (http://0.0.0.0:8080/auth/login)
  - Use the default user and password "airflow" or the ones at the .env file `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD`
  - <img width="700" height="490" alt="image" src="https://github.com/user-attachments/assets/93bea16d-53d7-4833-b7f9-146ba95e2430" />

7. Trigger the `idfm_setup_schema` DAG to initialize the DB base tables

---

Now everything is set to run all the ETL DAGs available.
<img width="1163" height="999" alt="image" src="https://github.com/user-attachments/assets/2cba5991-6f7e-49d1-96fb-b225a8741d9b" />

---

## Future features

- Remove Pandas to a more scalable PySpark implementation
- The YAML config file for the DAGs will be expanded upon, similar to the [Astronomer.io](https://github.com/astronomer/dag-factory) DAG factory and this [AWS blog](https://aws.amazon.com/blogs/big-data/dynamic-dag-generation-with-yaml-and-dag-factory-in-amazon-mwaa/) post.
- Create Data Warehouses and data quality checks.
- Set up the workflow and storage at a cloud service.
- Create dashboards and extract information.
