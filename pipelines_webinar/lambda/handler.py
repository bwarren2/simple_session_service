import logging, os

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    return {"body": "Hello from limmy lams", "statusCode": "200"}
