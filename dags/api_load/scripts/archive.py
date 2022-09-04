import os
import psycopg2
import json
import datetime
from api_load.scripts.upload_s3 import upload_to_s3

DB_URI = os.environ["AIRFLOW_CONN_AD_DATABASE"]
# A single filename for a particular run.
filename = (
    "postgres_backup_"
    + str(datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S"))
    + ".json"
)


def write_to_file(data):
    """
    This method takes the data from postgresql, converts into a python dictionary and write to a json file.
    It calls the generic python code 'upload_to_s3' to upload the generated json file to archive folder of s3 bucket
    Parameters : data
                    type : int
                    description : data from postgresql
    Return : None

    """
    with open(filename, "w") as write_file:
        for d in data:
            data_dict = {}
            data_dict["ad_id"] = d[0]
            data_dict["ad_group"] = d[1]
            data_dict["ad_campaign"] = d[2]
            data_dict["ad_scheme"] = d[3]
            data_dict["shown_at"] = d[4]
            data_dict["inserted_at"] = d[5]
            write_file.write(json.dumps(data_dict, default=str))
            write_file.write("\n")
    # Call upload to s3 to upload the file to achive folder
    upload_to_s3(filename, f"archive/{filename}")


def archive():
    """
    This method reads data from Postgresql and stores the data as python list which is send to write_to_file
    function to further process and upload to S3 bucket.
    """
    conn = psycopg2.connect(DB_URI)
    sql_stmt = "select * from api_ad_data where shown_at < current_timestamp"
    with conn.cursor() as cur:
        cur.execute(sql_stmt)
        output = cur.fetchall()
        # Calling the write_to_file function only when some data is received by query execution to prevent creation
        # of empty files in S3 location
        if output:
            write_to_file(output)

    conn.close()

