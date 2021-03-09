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
            "SessionToken": {"S": str(session.uid)},
            "Username": {"S": session.username},
            "CreatedAt": {"S": str(session.created_at)},
            "ExpiresAt": {"S": str(session.expires_at)},
            "TTL": {"N": str(session.ttl)},
        },
        ConditionExpression="attribute_not_exists(SessionToken)",
    )
    logger.info(item)
    return {"body": str(session), "statusCode": "201"}


def listing(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

    table = dynamodb.Table("Pre-Prod-WebService-SessionTableA016F679-5QR7WFPT3FG")
    response = table.scan(
        TableName=os.getenv("SESSION_TABLE_NAME"),
        ScanIndexForward=True,
        Limit=10,
        FilterExpression="#DYNOBASE_Username = :Username",
        ExpressionAttributeNames={"#DYNOBASE_Username": "Username"},
        ExpressionAttributeValues={":Username": "ben"},
    )
    logger.info(response)
    return {"body": "a list", "statusCode": "200"}


def retrieve(event, context):
    client = boto3.client("dynamodb")
    response = client.get_item(
        TableName=os.getenv("SESSION_TABLE_NAME"),
        Key={"SessionToken": {"S": "f5d5189c-6a07-4666-85ae-797029cc3862"}},
    )
    logger.info(response)
    return {"body": "a retrieve", "statusCode": "200"}


def hello(event, context):
    return {"body": "Hello from lambda", "statusCode": "200"}
