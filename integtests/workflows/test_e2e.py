import requests
import os
from datetime import datetime


def test_create_read_delete():
    # Create a token for Ben
    with requests.post(
        os.environ["SERVICE_URL"] + "/sessions/", json={"username": "jason"}
    ) as response:
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "jason"
        jason_token = data["session_token"]

    # Create a token for John
    with requests.post(
        os.environ["SERVICE_URL"] + "/sessions/", json={"username": "parhum"}
    ) as response:
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "parhum"
        parhum_token = data["session_token"]

    # Get a list with them both
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
        assert response.status_code == 200
        assert jason_token in [x["session_token"] for x in response.json()]
        assert parhum_token in [x["session_token"] for x in response.json()]
    # Get them individually

    # Delete one

    # See it is gone

    # Delete the other

    # Both are gone.
