from fastapi.testclient import TestClient
from unittest.mock import patch
import os

from .main import app

# Client that raises server exceptions (default behavior)
client = TestClient(app)

# Client that does NOT raise server exceptions (for testing error responses)
client_no_raise = TestClient(app, raise_server_exceptions=False)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestPingEndpoint:
    """Tests for /ping endpoint with chaos testing behavior."""

    def test_ping_chaos_disabled_returns_200(self, monkeypatch):
        """When ENABLE_CHAOS_TESTING is not set, /ping should always return 200."""
        # Ensure env var is not set
        monkeypatch.delenv("ENABLE_CHAOS_TESTING", raising=False)

        # Test multiple times to ensure consistency
        for _ in range(5):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_chaos_disabled_false_returns_200(self, monkeypatch):
        """When ENABLE_CHAOS_TESTING=false, /ping should always return 200."""
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "false")

        for _ in range(5):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_chaos_disabled_invalid_value_returns_200(self, monkeypatch):
        """When ENABLE_CHAOS_TESTING has invalid value, /ping should always return 200."""
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "yes")

        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

    def test_ping_chaos_enabled_time_mod3_zero_returns_500(self, monkeypatch):
        """When chaos enabled and time()%3==0, /ping should return 500."""
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "true")

        # Mock time.time() to return value where int(time) % 3 == 0
        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            assert response.status_code == 500

    def test_ping_chaos_enabled_time_mod3_nonzero_returns_200(self, monkeypatch):
        """When chaos enabled and time()%3!=0, /ping should return 200."""
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "true")

        # Mock time.time() to return value where int(time) % 3 != 0
        with patch("app.main.time.time", return_value=4.0):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

        # Also test another non-zero mod value
        with patch("app.main.time.time", return_value=5.0):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_chaos_enabled_case_insensitive(self, monkeypatch):
        """ENABLE_CHAOS_TESTING should be case-insensitive."""
        # Test uppercase TRUE
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "TRUE")

        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            assert response.status_code == 500

        # Test mixed case TrUe
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "TrUe")

        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            assert response.status_code == 500

    def test_ping_env_evaluated_per_request(self, monkeypatch):
        """Environment variable should be evaluated per request, not at import time."""
        # Start with chaos disabled
        monkeypatch.delenv("ENABLE_CHAOS_TESTING", raising=False)

        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            # Should return 200 because chaos is disabled
            assert response.status_code == 200

        # Now enable chaos
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "true")

        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            # Should return 500 now because chaos is enabled
            assert response.status_code == 500

        # Disable again
        monkeypatch.setenv("ENABLE_CHAOS_TESTING", "false")

        with patch("app.main.time.time", return_value=3.0):
            response = client_no_raise.get("/ping")
            # Should return 200 again
            assert response.status_code == 200
