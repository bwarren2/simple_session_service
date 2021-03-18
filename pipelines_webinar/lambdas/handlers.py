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
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    item = table.put_item(
        Item={
            "SessionToken": str(session.uid),
            "Username": session.username,
            "CreatedAt": str(session.created_at),
            "ExpiresAt": str(session.expires_at),
            "TTL": str(session.ttl),
        },
        ConditionExpression="attribute_not_exists(SessionToken)",
        ReturnValues="ALL_NEW",
    )
    logger.info("Got back:")
    logger.info(item)
    logger.info("Done")
    return {"body": str(session), "statusCode": "201"}


def listing(event, context):
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.query(
        KeyConditionExpression="#DYNOBASE_SessionToken = :pkey",
        ExpressionAttributeNames={"#DYNOBASE_SessionToken": "SessionToken"},
        ExpressionAttributeValues={":pkey": "f5d5189c-6a07-4666-85ae-797029cc3862"},
    )
    logger.info(response)
    return {"body": "a list", "statusCode": "200"}


def retrieve(event, context):
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.get_item(
        Key={"SessionToken": event["pathParameters"]["item"]},
    )
    logger.info(response)
    return {"body": "a retrieve", "statusCode": "200"}


def hello(event, context):
    return {"body": "Hello from lambda", "statusCode": "200"}
