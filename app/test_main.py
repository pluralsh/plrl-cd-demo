from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("timestamp", [0, 1, 3, 4, 6])
def test_ping_is_successful_for_all_clock_values(monkeypatch, timestamp):
    # The prior handler failed whenever int(time.time()) % 3 == 0.
    monkeypatch.setattr(
        main, "time", SimpleNamespace(time=lambda: timestamp), raising=False
    )

    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
