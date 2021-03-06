import logging
import json
from sessions import schemas

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)

import os

print(os.path)

for root, dirs, files in os.walk("."):
    for filename in files:
        print(filename)


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

    return {"body": str(session), "statusCode": "201"}


def listing(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "a list", "statusCode": "200"}


def hello(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "Hello from lambda", "statusCode": "200"}
