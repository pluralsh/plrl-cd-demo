from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_ping_succeeds_at_formerly_failing_epoch_second():
    # The previous handler raised whenever the epoch second was divisible by three.
    with patch("time.time", return_value=1_700_000_001):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
