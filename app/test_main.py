from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_for_all_former_time_branches():
    for timestamp in (0, 1, 2):
        with patch("time.time", return_value=timestamp):
            response = client.get("/ping")

        assert response.status_code == 200
        assert response.json() == {"pong": True}
