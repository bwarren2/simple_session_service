import logging

logger = logging.getLogger("handler")


def handler(event, context):
    logger.info(event, context)
    return {"body": "Hello from limmy lams", "statusCode": "200"}
