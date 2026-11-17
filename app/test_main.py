from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_at_previously_failing_epoch_second():
    epoch_second = 1_700_000_001
    assert epoch_second % 3 == 0

    with patch("time.time", return_value=epoch_second):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
