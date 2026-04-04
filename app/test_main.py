import os
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from .main import app, is_chaos_mode_enabled

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestHealthzEndpoint:
    """Tests for the /healthz stable health endpoint."""

    def test_healthz_returns_200(self):
        """Verify /healthz always returns HTTP 200."""
        response = client.get("/healthz")
        assert response.status_code == 200

    def test_healthz_returns_ok_body(self):
        """Verify /healthz returns 'ok' in the response body."""
        response = client.get("/healthz")
        assert response.text == "ok"

    def test_healthz_content_type_is_plain_text(self):
        """Verify /healthz returns plain text content type."""
        response = client.get("/healthz")
        assert "text/plain" in response.headers.get("content-type", "")


class TestPingEndpointDefault:
    """Tests for /ping endpoint with CHAOS_MODE disabled (default)."""

    def test_ping_returns_200_when_chaos_mode_unset(self):
        """Verify /ping returns 200 when CHAOS_MODE is not set."""
        # Ensure CHAOS_MODE is not set
        with patch.dict(os.environ, {}, clear=True):
            # Remove CHAOS_MODE if it exists
            os.environ.pop('CHAOS_MODE', None)
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_returns_200_when_chaos_mode_false(self):
        """Verify /ping returns 200 when CHAOS_MODE=false."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'false'}):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_returns_200_when_chaos_mode_empty(self):
        """Verify /ping returns 200 when CHAOS_MODE is empty string."""
        with patch.dict(os.environ, {'CHAOS_MODE': ''}):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}


class TestPingEndpointChaosMode:
    """Tests for /ping endpoint with CHAOS_MODE enabled."""

    def test_ping_can_fail_when_chaos_mode_true(self):
        """Verify /ping raises exception when CHAOS_MODE=true and time condition met."""
        import app.main as main_module
        original_time = main_module.time.time
        try:
            # Mock time.time() to return a value divisible by 3
            main_module.time.time = lambda: 3.0
            with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
                # The endpoint raises an exception, which TestClient re-raises
                with pytest.raises(Exception, match="unknown internal error"):
                    client.get("/ping")
        finally:
            main_module.time.time = original_time

    def test_ping_succeeds_when_chaos_mode_true_but_time_not_divisible(self):
        """Verify /ping returns 200 when CHAOS_MODE=true but time condition not met."""
        import app.main as main_module
        original_time = main_module.time.time
        try:
            # Mock time.time() to return a value NOT divisible by 3
            main_module.time.time = lambda: 1.0
            with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
                response = client.get("/ping")
                assert response.status_code == 200
                assert response.json() == {"pong": True}
        finally:
            main_module.time.time = original_time

    def test_ping_chaos_mode_case_insensitive(self):
        """Verify CHAOS_MODE check is case insensitive."""
        import app.main as main_module
        original_time = main_module.time.time
        try:
            main_module.time.time = lambda: 3.0
            with patch.dict(os.environ, {'CHAOS_MODE': 'TRUE'}):
                # The endpoint raises an exception, which TestClient re-raises
                with pytest.raises(Exception, match="unknown internal error"):
                    client.get("/ping")
        finally:
            main_module.time.time = original_time


class TestChaosModeHelper:
    """Tests for the is_chaos_mode_enabled helper function."""

    def test_chaos_mode_disabled_by_default(self):
        """Verify chaos mode is disabled when env var is not set."""
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop('CHAOS_MODE', None)
            assert is_chaos_mode_enabled() is False

    def test_chaos_mode_enabled_when_true(self):
        """Verify chaos mode is enabled when CHAOS_MODE=true."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'true'}):
            assert is_chaos_mode_enabled() is True

    def test_chaos_mode_disabled_when_false(self):
        """Verify chaos mode is disabled when CHAOS_MODE=false."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'false'}):
            assert is_chaos_mode_enabled() is False

    def test_chaos_mode_enabled_case_insensitive(self):
        """Verify CHAOS_MODE=TRUE (uppercase) enables chaos mode."""
        with patch.dict(os.environ, {'CHAOS_MODE': 'TRUE'}):
            assert is_chaos_mode_enabled() is True

        with patch.dict(os.environ, {'CHAOS_MODE': 'True'}):
            assert is_chaos_mode_enabled() is True
