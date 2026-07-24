import importlib

from fastapi.testclient import TestClient
import prometheus_client as prom

from . import main


def create_client(monkeypatch, ping_chaos_enabled=None):
    monkeypatch.setattr(prom, "start_http_server", lambda *args, **kwargs: None)

    if ping_chaos_enabled is None:
        monkeypatch.delenv("PING_CHAOS_ENABLED", raising=False)
    else:
        monkeypatch.setenv("PING_CHAOS_ENABLED", ping_chaos_enabled)

    reloaded_main = importlib.reload(main)
    return TestClient(reloaded_main.app)


def test_read_root(monkeypatch):
    client = create_client(monkeypatch)
    response = client.get("/")
    assert response.status_code == 200


def test_ping_defaults_healthy(monkeypatch):
    client = create_client(monkeypatch)
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"pong": True}
