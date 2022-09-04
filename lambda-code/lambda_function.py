import logging
import psycopg2
import base64
import json
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
def lambda_handler(event, context):
    for record in event['Records']:
       #Kinesis data is base64 encoded so decode here
       payload=base64.b64decode(record["kinesis"]["data"])
       print(payload)
    # conn = psycopg2.connect(
    # host="34.202.163.219",
    # database="airflow",
    # user="airflow",
    # password="airflow")
    # logging.info('Lambda in LocalStack')
    # cur = conn.cursor()
    # cur.execute('SELECT version()')
    # db_version = cur.fetchone()
    # logging.info(db_version)
    # return {
    #     "message": db_version
    # }