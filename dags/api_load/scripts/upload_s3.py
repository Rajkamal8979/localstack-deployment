import boto3

s3 = boto3.resource(
    "s3",
    aws_access_key_id="something_not_empty",
    aws_secret_access_key="something_not_empty",
    endpoint_url="http://localhost:4566"
)
bucket_name = "ad-data"


def upload_to_s3(filename, key):
    """
    This method uploads the file to the location specified by 'key' in S3 bucket
    Parameters :
                filename:
                    type : str
                    description : filename of the locally generated file that will be uploaded to S3
                key:
                    type : str
                    description : key name that will be used to create a file in S3 bucket
    """
    # A basic try and catch block to handle any exception occcurred while operations to S3
    try:
        s3.Bucket(bucket_name).upload_file(filename, key)
    except Exception as e:
        print("Exception occured while uploading to S3", e)

