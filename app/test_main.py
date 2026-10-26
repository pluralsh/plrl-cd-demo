from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong():
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_hello_returns_expected_payload():
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}


def test_world_returns_expected_payload():
    response = client.get("/world")

    assert response.status_code == 200
    assert response.json() == {"world": "hello!"}


def test_user_returns_expected_payload():
    response = client.get("/user")

    assert response.status_code == 200
    assert response.json() == {"user:": "bob"}
