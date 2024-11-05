from boto3 import client as boto3_client

def handler(event, context):
    print("Event: ", event)
    return {"statusCode": 200, "body": "Hello from Lambda"}
