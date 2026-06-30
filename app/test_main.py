from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_healthy():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_ping_is_stable_across_repeated_requests():
    responses = [client.get("/ping") for _ in range(5)]

    assert all(response.status_code == 200 for response in responses)
    assert all(response.json() == {"pong": True} for response in responses)
