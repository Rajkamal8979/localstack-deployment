import logging
import psycopg2
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
def lambda_handler(event, context):
    conn = psycopg2.connect(
    host="34.202.163.219",
    database="airflow",
    user="airflow",
    password="airflow")
    logging.info('Lambda in LocalStack')
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    logging.info(db_version)
    return {
        "message": db_version
    }