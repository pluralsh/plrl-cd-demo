from fastapi.testclient import TestClient

from . import main
from .main import app



def test_read_root():
    response = TestClient(app).get("/")
    assert response.status_code == 200



def test_ping_returns_success_by_default(monkeypatch):
    monkeypatch.delenv(main.PING_FAILURE_MODE_ENV, raising=False)
    response = TestClient(app).get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}



def test_ping_can_opt_into_time_based_failure(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_MODE_ENV, main.PING_FAILURE_MODE_TIME_BASED)
    monkeypatch.setattr(main.time, "time", lambda: 3)
    response = TestClient(app, raise_server_exceptions=False).get("/ping")

    assert response.status_code == 500



def test_ping_opt_in_mode_still_succeeds_when_failure_condition_not_met(monkeypatch):
    monkeypatch.setenv(main.PING_FAILURE_MODE_ENV, main.PING_FAILURE_MODE_TIME_BASED)
    monkeypatch.setattr(main.time, "time", lambda: 4)
    response = TestClient(app).get("/ping")

    assert response.status_code == 200
    assert response.json() == {"pong": True}
