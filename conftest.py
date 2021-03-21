import boto3
import sys
import os
import logging

logger = logging.getLogger()

here = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "pipelines_webinar", "lambdas"
)
sys.path.insert(0, here)


def pytest_sessionstart(session):
    logger.info(f"Purging test table: {os.environ['SERVICE_URL']}")
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.scan(Limit=30)
    for item in response["Items"]:
        table.delete_item(
            Key={"session_token": item["session_token"]},
        )
    remaining = table.scan(Limit=30)
    assert len(remaining["Items"]) == 0
