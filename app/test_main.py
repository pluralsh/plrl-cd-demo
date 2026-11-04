from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_when_former_time_based_failure_condition_matches():
    # The former implementation raised when int(time.time()) was divisible by 3.
    with patch("time.time", return_value=3):
        for _ in range(3):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}
