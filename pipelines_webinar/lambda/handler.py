import logging

logging.getLogger("handler")


def handler(event, context):
    logger.info("Invoked ze lambda")
    return {"body": "Hello king from limmy lams", "statusCode": "200"}
