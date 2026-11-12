from fastapi.testclient import TestClient
from unittest.mock import patch

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_previously_failing_clock_value():
    # A timestamp divisible by three previously raised an internal exception.
    with patch("time.time", return_value=3):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
