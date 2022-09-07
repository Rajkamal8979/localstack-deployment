import json, boto3
import random
import time
kinesis_client = boto3.client('kinesis',region_name = 'us-east-1',endpoint = 'http://0.0.0.0:4566')

def put_to_stream_org(event_uuid,name,organization_uuid,organization_name,subscription_plan,locale,created_at):
    payload = {}
    payload["event_uuid"] = event_uuid
    payload["name"] = name
    payload["organization_uuid"] = organization_uuid
    payload["organization_name"] = organization_name
    payload["subscription_plan"]= subscription_plan
    payload["locale"] = locale
    payload["created_at"]= created_at
    print(json.dumps(payload))
    put_response = kinesis_client.put_record(
    StreamName='my-stream',
    Data=json.dumps(payload),
    PartitionKey=event_uuid
    )
def put_to_stream_org_role(event_uuid,name,role_uuid,role_name,organization_uuid,created_at):
    payload = {}
    payload["event_uuid"] = event_uuid
    payload["name"] = name
    payload["role_uuid"] = role_uuid
    payload["role_name"] = role_name
    payload["organization_uuid"] = organization_uuid
    payload["created_at"]= created_at
    print(json.dumps(payload))
    put_response = kinesis_client.put_record(
    StreamName='my-stream',
    Data=json.dumps(payload),
    PartitionKey=event_uuid
    )

def generate_org_rec():
    event_uuid = "0123456789abcdef0123456789abcdef"
    name = "organization:created"
    organization_uuid = "eaebc4fd-1231-4ead-9e4e-db9f452580e7"
    organization_name = "Test Organization 2"
    subscription_plan = 'abc'
    locale = "eu"
    created_at =  "2019-09-06T07:54:45.000Z"
    put_to_stream_org(event_uuid,name,organization_uuid,organization_name,subscription_plan,locale,created_at)

def generate_role():
    event_uuid = "0123456789abcdef0123456789abcdef"
    name = "organization_role:created"
    role_uuid = "eaebc4fd-1231-4ead-9e4e-db9f452580e7"
    role_name = "organization_member-2"
    organization_uuid = "eaebc4fd-1231-4ead-9e4e-db9f452580e7"
    created_at =  "2019-09-06T07:54:45.000Z"

    put_to_stream_org_role(event_uuid,name,role_uuid,role_name,organization_uuid,created_at)


generate_org_rec()
generate_role()

