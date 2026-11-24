import time

import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("previously_failing_epoch", [0, 3, 1735689600])
def test_ping_succeeds_at_previously_failing_clock_values(monkeypatch, previously_failing_epoch):
    """Multiples of three previously made /ping return an HTTP 500."""
    monkeypatch.setattr(time, "time", lambda: previously_failing_epoch)

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
