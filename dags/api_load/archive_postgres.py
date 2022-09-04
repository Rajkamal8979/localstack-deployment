from datetime import datetime
from api_load.scripts.archive import archive
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    "achive-and-delete-from-postgres",
    description="This DAG achives the old data to S3 bucket and deletes it from database",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule_interval='@daily',
) as dag:
    archive_table = PythonOperator(
        task_id="archive_data",
        python_callable=archive,
    )
    delete_from_table = PostgresOperator(
        task_id="delete_from_table",
        postgres_conn_id="ad_database",
        sql="""
        DELETE FROM api_ad_data where shown_at < current_timestamp
        """,
    )

archive_table >> delete_from_table
