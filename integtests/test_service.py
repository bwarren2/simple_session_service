import requests
import os


def test_root():
    with requests.get(os.environ["SERVICE_URL"]) as response:
        assert response.status_code == 200
        assert response.content == b"Hello from lambda"


def test_list():
    with requests.get(os.environ["SERVICE_URL"] + "/sessions/") as response:
        assert response.status_code == 200
        assert response.content == b"a list"


def test_create():
    with requests.post(
        os.environ["SERVICE_URL"] + "/sessions/", json={"username": "ben"}
    ) as response:
        assert response.status_code == 201
