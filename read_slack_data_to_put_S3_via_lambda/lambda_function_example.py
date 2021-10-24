import json
import boto3
import os
from slack_sdk import WebClient

def lambda_handler(event, context):

    token_str = "{SLACK_API_TOKEN}"
    client = WebClient(token=token_str)
    response = client.conversations_history(channel="{SLACK_CHANNEL_CODE}")

    with open('/tmp/{FILE_NAME}','w') as outfile:
        json.dump(response['messages'], outfile, indent=4)

    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/{FILE_NAME}','{BUCKET_NAME}', '{FILE_NAME}')
    os.remove('/tmp/{FILE_NAME}')

    return {
        'statusCode': 200,
        'body': json.dumps("success")
    }
