from fastapi.testclient import TestClient
from unittest.mock import patch

from .main import app

client = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


def test_ping_returns_200_by_default():
    """Test that /ping returns 200 when SIMULATE_FAILURES is not set."""
    with patch.dict("os.environ", {}, clear=True):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_ping_returns_200_when_simulate_failures_false():
    """Test that /ping returns 200 when SIMULATE_FAILURES=false."""
    with patch.dict("os.environ", {"SIMULATE_FAILURES": "false"}):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_ping_fails_when_simulate_failures_enabled_and_time_divisible_by_3(monkeypatch):
    """Test that /ping returns 500 when SIMULATE_FAILURES=true and time.time() % 3 == 0."""
    monkeypatch.setenv("SIMULATE_FAILURES", "true")
    # Mock time.time() to return a value divisible by 3
    with patch("app.main.time.time", return_value=9):
        response = client.get("/ping")
        assert response.status_code == 500


def test_ping_succeeds_when_simulate_failures_enabled_and_time_not_divisible_by_3(monkeypatch):
    """Test that /ping returns 200 when SIMULATE_FAILURES=true but time.time() % 3 != 0."""
    monkeypatch.setenv("SIMULATE_FAILURES", "true")
    # Mock time.time() to return a value NOT divisible by 3
    with patch("app.main.time.time", return_value=10):
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}


def test_fail_endpoint_returns_200_by_default():
    """Test that /fail returns 200 when SIMULATE_FAILURES is not set."""
    with patch.dict("os.environ", {}, clear=True):
        response = client.get("/fail")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert "disabled" in response.json()["message"]


def test_fail_endpoint_returns_200_when_simulate_failures_false():
    """Test that /fail returns 200 when SIMULATE_FAILURES=false."""
    with patch.dict("os.environ", {"SIMULATE_FAILURES": "false"}):
        response = client.get("/fail")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_fail_endpoint_fails_when_simulate_failures_enabled_and_time_divisible_by_3(monkeypatch):
    """Test that /fail returns 500 when SIMULATE_FAILURES=true and time.time() % 3 == 0."""
    monkeypatch.setenv("SIMULATE_FAILURES", "true")
    with patch("app.main.time.time", return_value=9):
        response = client.get("/fail")
        assert response.status_code == 500


def test_fail_endpoint_succeeds_when_simulate_failures_enabled_and_time_not_divisible_by_3(monkeypatch):
    """Test that /fail returns 200 when SIMULATE_FAILURES=true but time.time() % 3 != 0."""
    monkeypatch.setenv("SIMULATE_FAILURES", "true")
    with patch("app.main.time.time", return_value=10):
        response = client.get("/fail")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert "enabled but not triggered" in response.json()["message"]


def test_hello():
    """Test the /hello endpoint."""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}


def test_world():
    """Test the /world endpoint."""
    response = client.get("/world")
    assert response.status_code == 200
    assert response.json() == {"world": "hello!"}
