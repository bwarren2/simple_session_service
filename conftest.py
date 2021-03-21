import boto3
import sys
import os
import logging
import requests

logger = logging.getLogger()

here = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "session_tokens_app", "lambdas"
)
sys.path.insert(0, here)


def pytest_sessionstart(session):
    logger.info(f"Purging test table: {os.environ['SESSION_TABLE_NAME']}")
    table = boto3.resource("dynamodb").Table(os.getenv("SESSION_TABLE_NAME"))
    response = table.scan(Limit=30)
    for item in response["Items"]:
        table.delete_item(
            Key={"session_token": item["session_token"]},
        )
    remaining = table.scan(Limit=30)
    assert len(remaining["Items"]) == 0

    logger.warn(f"Purging test endpoint: {os.environ['SERVICE_URL']}")
    has_remaining = True
    while has_remaining == True:
        with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
            tokens = [x["session_token"] for x in response.json()]
            for token in tokens:
                logger.warn(f"Deleting {token}")
                with requests.delete(
                    os.environ["SERVICE_URL"] + "/sessions/" + token
                ) as response:
                    assert response.status_code == 204

        with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
            has_remaining = len([x["session_token"] for x in response.json()]) > 0
