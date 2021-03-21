import os
import logging
import json
import boto3
import decimal

from sessions import schemas

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


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
    item_data = schemas.SessionSchema().dump(session)
    json_string_data = schemas.SessionSchema().dumps(session)

    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.put_item(
        Item=item_data,
        ConditionExpression="attribute_not_exists(session_token)",
    )

    return {
        "body": json_string_data,
        "statusCode": "201",
        "headers": {"Content-Type": "application/json"},
    }


def listing(event, context):
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.scan(Limit=3)
    return {
        "body": json.dumps(response["Items"], cls=DecimalEncoder),
        "statusCode": "200",
    }


def retrieve(event, context):
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.get_item(
        Key={"session_token": event["pathParameters"]["item"]},
    )
    return {
        "body": json.dumps(response["Item"], cls=DecimalEncoder),
        "statusCode": "200",
    }


def delete(event, context):
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    table.delete_item(
        Key={"session_token": event["pathParameters"]["item"]},
    )
    return {
        "body": "",
        "statusCode": "204",
    }


def hello(event, context):
    return {"body": "Hello from lambda", "statusCode": "200"}
