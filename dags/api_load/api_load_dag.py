from datetime import datetime

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from api_load.scripts.load import load

with DAG(
    "api-load",
    description="This DAG loads data from an API regularly and stores them in the database",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule_interval="12 * * * *",
) as dag:
    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="ad_database",
        sql="""
        CREATE TABLE IF NOT EXISTS api_ad_data (
            ad_id TEXT PRIMARY KEY,
            ad_group TEXT NOT NULL,
            ad_campaign INTEGER NOT NULL,
            ad_scheme JSON NOT NULL,
            shown_at TIMESTAMP NOT NULL,
            inserted_at TIMESTAMP NOT NULL
        )
        """,
    )

    backup_insert_data = PythonOperator(
        task_id="backup_and_insert_data",
        python_callable=load,
    )

    create_table >> backup_insert_data
