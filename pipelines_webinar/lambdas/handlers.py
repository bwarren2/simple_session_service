import os
import logging
import json
import boto3

from sessions import schemas

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


def create(event, context):
    try:
        body = event["body"]
    except KeyError:
        return {"body": "Missing request body", "statusCode": "400"}

    try:
        json_body = json.loads(body)
    except json.JSONDecodeError:
        return {"body": "Invalid request body", "statusCode": "400"}
    session = schemas.SessionSchema().load(json_body)
    client = boto3.client("dynamodb")
    item = client.put_item(
        TableName=os.getenv("SESSION_TABLE_NAME"),
        Item={
            "SessionToken": {"S": session.uid},
            "Username": {"S": session.username},
            "CreatedAt": {"S": session.created_at},
            "ExpiresAt": {"S": session.expires_at},
            "TTL": {"N": session.ttl},
        },
        ConditionExpression="attribute_not_exists(SessionToken)",
    )
    logger.info(item)
    return {"body": str(session), "statusCode": "201"}


def listing(event, context):
    return {"body": "a list", "statusCode": "200"}


def hello(event, context):
    return {"body": "Hello from lambda", "statusCode": "200"}
