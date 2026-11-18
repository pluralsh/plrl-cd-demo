import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("former_failure_timestamp", [0, 3, 6])
def test_ping_returns_success_at_former_failure_timestamps(monkeypatch, former_failure_timestamp):
    # These timestamps satisfied the removed `int(time.time()) % 3 == 0` failure path.
    monkeypatch.setattr("time.time", lambda: former_failure_timestamp)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
