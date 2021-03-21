import requests
import os
from datetime import datetime


def test_create_read_delete():
    # Create a token for Ben
    with requests.post(
        os.environ["SERVICE_URL"] + "/sessions/", json={"username": "ben"}
    ) as response:
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "ben"
        ben_token = data["session_token"]

    # Create a token for John
    with requests.post(
        os.environ["SERVICE_URL"] + "/sessions/", json={"username": "john"}
    ) as response:
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "john"
        john_token = data["session_token"]

    # Get a list with them both
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
        assert response.status_code == 200
        assert ben_token in [x["session_token"] for x in response.json()]
        assert john_token in [x["session_token"] for x in response.json()]

    # Get them individually
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/" + ben_token) as response:
        assert response.status_code == 200

    with requests.get(os.environ["SERVICE_URL"] + "/sessions/" + ben_token) as response:
        assert response.status_code == 200

    # Delete one
    with requests.delete(
        os.environ["SERVICE_URL"] + "/sessions/" + ben_token
    ) as response:
        assert response.status_code == 204

    # See it is gone
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
        assert response.status_code == 200
        assert ben_token not in [x["session_token"] for x in response.json()]
        assert john_token in [x["session_token"] for x in response.json()]

    # Delete the other
    with requests.delete(
        os.environ["SERVICE_URL"] + "/sessions/" + john_token
    ) as response:
        assert response.status_code == 204

    # Both are gone.
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
        assert response.status_code == 200
        assert ben_token not in [x["session_token"] for x in response.json()]
        assert john_token not in [x["session_token"] for x in response.json()]
