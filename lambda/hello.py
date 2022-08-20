import json


def handler(event, context):
    print(f"request: {json.dumps(event)}")
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain",
        },
        "body": f"Good day CDK, you have hit the path {event['path']}",
    }
    return response
