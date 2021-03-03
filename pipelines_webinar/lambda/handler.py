import logging

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


def handler(event, context):
    logger.info(event)
    return {"body": "Hello from lambda", "statusCode": "200"}


def custom(event, context):
    logger.info(event)
    return {"body": "Goodbye from lambda", "statusCode": "200"}
