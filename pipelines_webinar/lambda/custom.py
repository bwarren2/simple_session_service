import logging

logger = logging.getLogger("handler")
logger.setLevel(logging.INFO)


def custom(event, context):
    logger.info(event)
    return {"body": "Goodbye from lambda", "statusCode": "200"}
