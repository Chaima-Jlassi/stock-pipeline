from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys 
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.extract import extract
from scripts.transform import transform
from scripts.load import create_table, load

default_args = {
    "owner": "chaima",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "email_on_failure": False,
}

with DAG(
    dag_id="stock_pipeline",
    default_args=default_args,
    description="Daily ETL pipeline for stock market data",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["finance", "etl"]
) as dag:
    def extract_task(**kwargs):
        df = extract()
        kwargs["ti"].xcom_push(key="raw_data", value=df.to_json())

    def transform_task(**kwargs):
        import pandas as pd
        raw_json = kwargs["ti"].xcom_pull(key="raw_data", task_ids="extract")
        df_raw = pd.read_json(raw_json)
        df_transformed = transform(df_raw)
        kwargs["ti"].xcom_push(key="transformed_data", value=df_transformed.to_json())
    
    def load_task(**kwargs):
        import pandas as pd
        transformed_json = kwargs["ti"].xcom_pull(key="transformed_data", task_ids="transform")
        df = pd.read_json(transformed_json)
        create_table()
        load(df)

    t1 = PythonOperator(task_id="extract",   python_callable=extract_task)
    t2 = PythonOperator(task_id="transform", python_callable=transform_task)
    t3 = PythonOperator(task_id="load",      python_callable=load_task)

    t1 >> t2 >> t3