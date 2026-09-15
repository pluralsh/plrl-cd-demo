from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_reliably_successful():
    for _ in range(5):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_error_fixture_returns_internal_server_error():
    response = client.get("/test/error")
    assert response.status_code == 500
    assert response.json() == {"detail": "unknown internal error"}
