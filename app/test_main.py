import time

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping():
    for request_number in range(4):
        response = client.get("/ping")

        assert response.status_code == 200
        assert response.json() == {"pong": True}
        if request_number < 3:
            time.sleep(1)
