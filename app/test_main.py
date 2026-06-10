from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_is_stable():
    statuses = {client.get("/ping").status_code for _ in range(5)}
    assert statuses == {200}
    assert client.get("/ping").json() == {"pong": True}
