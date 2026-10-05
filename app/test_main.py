from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_pong_at_former_failure_timestamp():
    # Timestamp 3 formerly triggered the intentional /ping 500 condition.
    with patch("time.time", return_value=3):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
