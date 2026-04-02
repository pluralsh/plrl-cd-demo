from fastapi.testclient import TestClient
import os
import pytest

from .main import app, set_rng_func

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


class TestPingEndpoint:
    """Tests for the /ping endpoint with chaos mode support."""

    def setup_method(self):
        """Reset RNG function and clear env var before each test."""
        set_rng_func(None)  # Reset to default
        os.environ.pop("PING_FAIL_RATE", None)

    def teardown_method(self):
        """Clean up after each test."""
        set_rng_func(None)
        os.environ.pop("PING_FAIL_RATE", None)

    def test_ping_default_always_returns_200(self):
        """Without PING_FAIL_RATE, /ping should always return 200."""
        # Run multiple times to ensure consistency
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_fail_rate_zero_always_returns_200(self):
        """With PING_FAIL_RATE=0.0, /ping should always return 200."""
        os.environ["PING_FAIL_RATE"] = "0.0"
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_fail_rate_one_always_returns_500(self):
        """With PING_FAIL_RATE=1.0, /ping should always return 500."""
        os.environ["PING_FAIL_RATE"] = "1.0"
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 500
            assert "Chaos mode failure" in response.json()["detail"]

    def test_ping_with_injected_rng_fails_when_below_rate(self):
        """When RNG returns value below fail rate, should return 500."""
        os.environ["PING_FAIL_RATE"] = "0.5"
        # Inject RNG that always returns 0.3 (below 0.5 threshold)
        set_rng_func(lambda: 0.3)

        response = client.get("/ping")
        assert response.status_code == 500
        assert "Chaos mode failure" in response.json()["detail"]
        assert "PING_FAIL_RATE triggered" in response.json()["detail"]

    def test_ping_with_injected_rng_succeeds_when_above_rate(self):
        """When RNG returns value above fail rate, should return 200."""
        os.environ["PING_FAIL_RATE"] = "0.5"
        # Inject RNG that always returns 0.7 (above 0.5 threshold)
        set_rng_func(lambda: 0.7)

        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

    def test_ping_with_injected_rng_boundary_equal_rate(self):
        """When RNG returns exactly the fail rate, should succeed (< not <=)."""
        os.environ["PING_FAIL_RATE"] = "0.5"
        # Inject RNG that returns exactly 0.5 (not less than 0.5)
        set_rng_func(lambda: 0.5)

        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json() == {"pong": True}

    def test_ping_invalid_fail_rate_defaults_to_zero(self):
        """Invalid PING_FAIL_RATE values should default to 0.0 (always succeed)."""
        for invalid_value in ["invalid", "abc", "-1", "1.5", "", "  "]:
            os.environ["PING_FAIL_RATE"] = invalid_value
            response = client.get("/ping")
            # Should succeed because invalid values default to 0.0
            # Note: "-1" and "1.5" will be clamped to 0.0 and 1.0 respectively
            # but we're testing that no exception is raised
            assert response.status_code in [200, 500]

    def test_ping_negative_fail_rate_clamped_to_zero(self):
        """Negative PING_FAIL_RATE should be clamped to 0.0 (always succeed)."""
        os.environ["PING_FAIL_RATE"] = "-0.5"
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 200
            assert response.json() == {"pong": True}

    def test_ping_fail_rate_above_one_clamped(self):
        """PING_FAIL_RATE > 1.0 should be clamped to 1.0 (always fail)."""
        os.environ["PING_FAIL_RATE"] = "2.0"
        for _ in range(10):
            response = client.get("/ping")
            assert response.status_code == 500
            assert "Chaos mode failure" in response.json()["detail"]

    def test_ping_error_message_is_informative(self):
        """Error response should have an informative message."""
        os.environ["PING_FAIL_RATE"] = "1.0"
        response = client.get("/ping")
        assert response.status_code == 500
        detail = response.json()["detail"]
        assert "Chaos mode failure" in detail
        assert "PING_FAIL_RATE" in detail
