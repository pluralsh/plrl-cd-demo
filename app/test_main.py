from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_deterministic_and_healthy():
    responses = [client.get("/ping") for _ in range(3)]

    for response in responses:
        assert response.status_code == 200
        assert response.json() == {"pong": True}
