from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_ping_succeeds_at_former_clock_failure():
    formerly_failing_epoch_second = 1_704_067_200
    assert formerly_failing_epoch_second % 3 == 0

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
