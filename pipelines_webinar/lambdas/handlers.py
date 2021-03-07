import os
import sys
import logging
import json

# from sessions import schemas

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


logger.info("Sys.path:")
logger.info(sys.path)
logger.info("OS.path:")
logger.info(os.path)

logger.info("Walk of opt/:")
for root, dirs, files in os.walk("/opt"):
    for filename in files:
        logger.info(dirs)
        logger.info(filename)

logger.info("##")
logger.info(os.listdir("/opt/python"))
logger.info(os.listdir("."))
logger.info(os.listdir("sessions"))
# logger.info(os.listdir("sessions/deps"))
logger.info("##")


def create(event, context):
    try:
        body = event["body"]
    except KeyError:
        return {"body": "Missing request body", "statusCode": "400"}

    try:
        json_body = json.loads(body)
    except json.JSONDecodeError:
        return {"body": "Invalid request body", "statusCode": "400"}
    # session = schemas.SessionSchema().load(json_body)
    session = {}

    return {"body": str(session), "statusCode": "201"}


def listing(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "a list", "statusCode": "200"}


def hello(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "Hello from lambda", "statusCode": "200"}
