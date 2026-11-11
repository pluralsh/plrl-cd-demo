from unittest.mock import patch

from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_succeeds_at_previously_failing_clock_boundary():
    # The previous implementation raised when int(time.time()) was divisible by 3.
    # Freeze that former failure condition so this regression test remains deterministic.
    with patch("time.time", return_value=1_700_000_001):
        response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
