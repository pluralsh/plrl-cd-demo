from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

from . import main
from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("mocked_epoch", [0, 1, 2, 3, 1_700_000_001])
def test_ping_succeeds_for_each_mocked_time(monkeypatch, mocked_epoch):
    monkeypatch.setattr(
        main,
        "time",
        SimpleNamespace(time=lambda: mocked_epoch),
        raising=False,
    )

    response = TestClient(app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
