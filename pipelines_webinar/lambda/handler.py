import logging

logging.getLogger("handler")


def handler(event, context):
    logger.info(event, context)
    return {"body": "Hello king from limmy lams", "statusCode": "200"}
