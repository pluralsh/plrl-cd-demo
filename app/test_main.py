from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_always_successful():
    responses = [client.get("/ping") for _ in range(3)]

    assert [response.status_code for response in responses] == [200, 200, 200]
    assert [response.json() for response in responses] == [{"pong": True}] * 3
