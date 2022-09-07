from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    "Snapshot_tables",
    description="This DAG PERFORMS UPSERTS ON SNAPSHOT TABLES",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule_interval= None,
) as dag:
    snap_organization_role_summary_snap = PostgresOperator(
        task_id="snap_organization_role_summary_snap",
        postgres_conn_id="ad_database",
        sql="sql/snap_organization_role_summary_snap.sql"
    )

    snap_organization_role_snap = PostgresOperator(
        task_id="snap_organization_role_snap",
        postgres_conn_id="ad_database",
        sql="sql/snap_organization_role_snap.sql"
    )

snap_organization_role_snap >> snap_organization_role_summary_snap
