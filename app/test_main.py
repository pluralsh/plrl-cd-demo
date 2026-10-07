from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@patch("time.time", return_value=1728000000)
def test_ping_returns_pong_at_former_failure_time(_mock_time):
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
