import logging
import psycopg2
from psycopg2.extras import execute_values
import base64
import json
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def create_connection():
    connection = psycopg2.connect(
        host="0.0.0.0",
        database="airflow",
        user="airflow",
        password="airflow"
        )
    return connection
  
def organization_insert(content):
    insert_template = "(%(event_uuid)s,%(name)s,%(organization_uuid)s,%(organization_name)s,%(subscription_plan)s,%(operation)s,%(locale)s,%(created_at)s)"
    sql_insert_query = """ INSERT INTO organization (event_uuid, name, organization_uuid,organization_name,subscription_plan,operation,locale,created_at) VALUES %s"""
    conn = create_connection()
    with conn.cursor() as cur:
        execute_values(cur, sql_insert_query, [content], template=insert_template)
    conn.commit()
    conn.close()
  
def organization_role_insert(content):
    insert_template = "(%(event_uuid)s,%(name)s,%(role_uuid)s,%(role_name)s,%(organization_uuid)s,%(operation)s,%(created_at)s)"
    sql_insert_query = """ INSERT INTO organization_role (event_uuid, name, role_uuid,role_name,organization_uuid,operation,created_at) VALUES %s"""
    conn = create_connection()
    with conn.cursor() as cur:
        execute_values(cur, sql_insert_query, [content], template=insert_template)
    conn.commit()
    conn.close()
  
def lambda_handler(event, context):
    print(event)
    for record in event['Records']:
        payload=base64.b64decode(record["kinesis"]["data"])
    print(payload)
    new_load = json.loads(payload)
    db_load = {}
    for k,v in new_load.items():
        if k == 'name':
            db_load['operation'] = v.split(":")[1]
            db_load['name'] = v
        db_load[k]= v
    print(db_load)
    if db_load['name'].split(":")[0] == 'organization':
        try:
            organization_insert(db_load)
            print("Data inserted for organization")
        except Exception as e:
            print(e)
    else:
        try:
            organization_role_insert(db_load)
            print("Data inserted for organization role")
        except Exception as e:
            print(e)
