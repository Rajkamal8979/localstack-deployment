import logging
import psycopg2
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

conn = psycopg2.connect(
    host="34.202.163.219",
    database="airflow",
    user="airflow",
    password="airflow")
def lambda_handler(event, context):
    logging.info('Lambda in LocalStack')
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    logging.info(db_version)
    return {
        "message": db_version
    }