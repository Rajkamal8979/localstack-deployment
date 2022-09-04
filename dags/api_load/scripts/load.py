import os
from api_load.scripts.extract import get_api_response
import psycopg2
import json
import datetime
from psycopg2.extras import execute_values
from api_load.scripts.upload_s3 import upload_to_s3

DB_URI = os.environ["AIRFLOW_CONN_AD_DATABASE"]

# insert template to map the key-value pairs in the data base execute method
insert_template = "(%(ad_id)s,%(ad_group)s,%(ad_campaign)s,%(ad_scheme)s,%(shown_at)s,CURRENT_TIMESTAMP)"
# query to be used to insert records from the API into database
insert_query = """INSERT INTO api_ad_data (ad_id, ad_group, ad_campaign, ad_scheme, shown_at, inserted_at) VALUES %s"""


def insert_to_db(new_data):
    """
    This method connects to Postgresql DB and inserts records bsaed on the insert_template
    """
    conn = psycopg2.connect(DB_URI)
    with conn.cursor() as cur:
        execute_values(cur, insert_query, new_data, template=insert_template)
    conn.commit()
    conn.close()


def load():
    """
    This method is invoked in api_load_dag.py
    It fetches records from API, processed them for the required changes based on the DB table structure,
    backup the received data in S3 bucket and insert records in database
    
    """
    api_response_data = get_api_response()
    filename = (
        "api_response_"
        + str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S"))
        + ".json"
    )
    for data in api_response_data:
        with open(filename, "w") as write_file:
            write_file.write(json.dumps(data))
    upload_to_s3(filename, f"backup/{filename}")

    new_data = []
    for d in api_response_data:
        d["shown_at"] = datetime.datetime.fromtimestamp(d["shown_at"]).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        if isinstance(d["ad_campaign"], str):
            d["ad_campaign"] = -1
        if "ad_scheme" not in d.keys():
            d["ad_scheme"] = json.dumps(None)
            new_data.append(d)
        else:
            d["ad_scheme"] = json.dumps(d["ad_scheme"])
            new_data.append(d)

    insert_to_db(new_data)
    return new_data

