import logging

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


def create(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "Goodbye from lambda", "statusCode": "201"}


def listing(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "a list", "statusCode": "200"}


def hello(event, context):
    logger.info(event)
    logger.info(context)
    return {"body": "Hello from lambda", "statusCode": "200"}
