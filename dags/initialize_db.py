from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


with DAG(
    "Initialize_tables",
    description="This DAG initializes all the tables",
    start_date=datetime(2022, 1, 1),
    catchup=False,
    schedule_interval= None,
) as dag:
    create_table_organization = PostgresOperator(
        task_id="create_table_organization",
        postgres_conn_id="ad_database",
        sql="sql/organization.sql"
    )

    create_table_organization_role = PostgresOperator(
        task_id="create_table_organization_role",
        postgres_conn_id="ad_database",
        sql="sql/organization_role.sql"
    )
    create_table_organization_role_snap = PostgresOperator(
        task_id="create_table_organization_role_snap",
        postgres_conn_id="ad_database",
        sql="sql/organization_role_snap.sql"
    )
    add_constraint_role_snap = PostgresOperator(
        task_id="add_constraint_role_snap",
        postgres_conn_id="ad_database",
        sql="""
        ALTER TABLE organization_role_snap
        ADD CONSTRAINT uniq_combination_role_snap UNIQUE(role_uuid,organization_uuid);
        """
        )
    add_constraint_role_summ_snap = PostgresOperator(
        task_id="add_constraint_role_summ_snap",
        postgres_conn_id="ad_database",
        sql="""
        ALTER TABLE organization_role_summary_snap
        ADD CONSTRAINT uniq_combination_role_summ_snap UNIQUE(role_uuid,organization_uuid);
        """
        )
    create_table_organization_role_summary_snap = PostgresOperator(
        task_id="create_table_organization_role_summary_snap",
        postgres_conn_id="ad_database",
        sql="sql/organization_role_summary_snap.sql"
        )
    create_table_organization >> create_table_organization_role >> create_table_organization_role_snap >> create_table_organization_role_summary_snap >> [add_constraint_role_snap,add_constraint_role_summ_snap]


