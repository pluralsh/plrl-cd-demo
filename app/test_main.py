from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_error_ping_is_opt_in():
    error_client = TestClient(app, raise_server_exceptions=False)
    response = error_client.get("/ping/error")
    assert response.status_code == 500
