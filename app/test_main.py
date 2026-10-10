from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_during_former_failure_second():
    # 1_700_000_001 is divisible by three and previously triggered a 500.
    with patch("time.time", return_value=1_700_000_001):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
