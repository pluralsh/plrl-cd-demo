from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)
error_client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_by_default():
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_intentional_ping_error_is_explicit():
    response = error_client.get("/ping/error")

    assert response.status_code == 500
