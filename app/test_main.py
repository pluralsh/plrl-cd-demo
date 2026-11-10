import time

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("epoch", [0, 3, 6])
def test_ping_succeeds_at_clock_boundaries(monkeypatch, epoch):
    monkeypatch.setattr(time, "time", lambda: epoch)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
