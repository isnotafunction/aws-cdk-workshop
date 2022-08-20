import json
import os

import boto3

ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["HITS_TABLE_NAME"])
lambda_ = boto3.client("lambda")


def handler(event, context):
    print(f"request: {json.dumps(event)}")
    table.update_item(
        Key={"path": event["path"]},
        UpdateExpression="ADD Hits :incr",
        ExpressionAttributeValues={":incr": 1},
    )

    response = lambda_.invoke(
        FunctionName=os.environ["DOWNSTREAM_FUNCTION_NAME"], Payload=json.dumps(event)
    )

    body = response["Payload"].read()

    print(f"Downstream response {body}")

    return json.loads(body)
