import time

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


@pytest.mark.parametrize("timestamp", [0, 1, 2, 3, 1_700_000_001])
def test_ping_always_returns_pong(monkeypatch, timestamp):
    monkeypatch.setattr(time, "time", lambda: timestamp)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
