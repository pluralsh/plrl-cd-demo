import pytest
from fastapi.testclient import TestClient

from .main import (
    app,
    parse_fault_inject_rate,
    parse_fault_inject_ping,
    DEFAULT_FAULT_INJECT_RATE,
    DEFAULT_FAULT_INJECT_PING,
)

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200


# =============================================================================
# Unit tests for parse_fault_inject_rate
# =============================================================================

class TestParseFaultInjectRate:
    """Tests for FAULT_INJECT_RATE parsing logic."""

    def test_none_returns_default(self):
        """Missing env var should return default."""
        assert parse_fault_inject_rate(None) == DEFAULT_FAULT_INJECT_RATE

    def test_empty_string_returns_default(self):
        """Empty string should return default."""
        assert parse_fault_inject_rate("") == DEFAULT_FAULT_INJECT_RATE
        assert parse_fault_inject_rate("   ") == DEFAULT_FAULT_INJECT_RATE

    def test_valid_float_values(self):
        """Valid float values should be parsed correctly."""
        assert parse_fault_inject_rate("0") == 0.0
        assert parse_fault_inject_rate("0.0") == 0.0
        assert parse_fault_inject_rate("0.5") == 0.5
        assert parse_fault_inject_rate("1") == 1.0
        assert parse_fault_inject_rate("1.0") == 1.0
        assert parse_fault_inject_rate("0.25") == 0.25

    def test_invalid_non_numeric_returns_default(self):
        """Non-numeric values should return default without crashing."""
        assert parse_fault_inject_rate("abc") == DEFAULT_FAULT_INJECT_RATE
        assert parse_fault_inject_rate("not_a_number") == DEFAULT_FAULT_INJECT_RATE
        assert parse_fault_inject_rate("1.2.3") == DEFAULT_FAULT_INJECT_RATE
        assert parse_fault_inject_rate("true") == DEFAULT_FAULT_INJECT_RATE

    def test_nan_returns_default(self):
        """NaN value should return default without crashing."""
        assert parse_fault_inject_rate("nan") == DEFAULT_FAULT_INJECT_RATE
        assert parse_fault_inject_rate("NaN") == DEFAULT_FAULT_INJECT_RATE

    def test_clamp_negative_to_zero(self):
        """Negative values should be clamped to 0."""
        assert parse_fault_inject_rate("-0.5") == 0.0
        assert parse_fault_inject_rate("-1") == 0.0
        assert parse_fault_inject_rate("-100") == 0.0

    def test_clamp_above_one_to_one(self):
        """Values above 1 should be clamped to 1."""
        assert parse_fault_inject_rate("1.5") == 1.0
        assert parse_fault_inject_rate("2") == 1.0
        assert parse_fault_inject_rate("100") == 1.0

    def test_does_not_crash_on_special_values(self):
        """Special float values should not crash."""
        # inf should be clamped to 1
        assert parse_fault_inject_rate("inf") == 1.0
        assert parse_fault_inject_rate("-inf") == 0.0


# =============================================================================
# Unit tests for parse_fault_inject_ping
# =============================================================================

class TestParseFaultInjectPing:
    """Tests for FAULT_INJECT_PING parsing logic."""

    def test_none_returns_default(self):
        """Missing env var should return default."""
        assert parse_fault_inject_ping(None) == DEFAULT_FAULT_INJECT_PING

    def test_empty_string_returns_default(self):
        """Empty string should return default."""
        assert parse_fault_inject_ping("") == DEFAULT_FAULT_INJECT_PING
        assert parse_fault_inject_ping("   ") == DEFAULT_FAULT_INJECT_PING

    def test_truthy_values(self):
        """Various truthy values should return True."""
        for val in ["true", "True", "TRUE", "1", "yes", "Yes", "YES", "on", "On", "ON"]:
            assert parse_fault_inject_ping(val) is True, f"Expected True for '{val}'"

    def test_falsy_values(self):
        """Various falsy values should return False."""
        for val in ["false", "False", "FALSE", "0", "no", "No", "NO", "off", "Off", "OFF"]:
            assert parse_fault_inject_ping(val) is False, f"Expected False for '{val}'"

    def test_invalid_values_return_default(self):
        """Invalid values should return default without crashing."""
        assert parse_fault_inject_ping("invalid") == DEFAULT_FAULT_INJECT_PING
        assert parse_fault_inject_ping("maybe") == DEFAULT_FAULT_INJECT_PING
        assert parse_fault_inject_ping("2") == DEFAULT_FAULT_INJECT_PING
        assert parse_fault_inject_ping("truee") == DEFAULT_FAULT_INJECT_PING

    def test_whitespace_handling(self):
        """Values with whitespace should be trimmed and parsed."""
        assert parse_fault_inject_ping("  true  ") is True
        assert parse_fault_inject_ping("  false  ") is False


# =============================================================================
# Integration tests for /healthz endpoint
# =============================================================================

class TestHealthzEndpoint:
    """Tests for the /healthz health check endpoint."""

    def test_healthz_returns_200(self):
        """Health endpoint should return 200 OK."""
        response = client.get("/healthz")
        assert response.status_code == 200

    def test_healthz_returns_json(self):
        """Health endpoint should return valid JSON."""
        response = client.get("/healthz")
        assert response.headers.get("content-type") == "application/json"
        data = response.json()
        assert data is not None

    def test_healthz_contains_status_ok(self):
        """Health endpoint should contain status: ok."""
        response = client.get("/healthz")
        data = response.json()
        assert data["status"] == "ok"

    def test_healthz_contains_fault_injection_config(self):
        """Health endpoint should contain fault injection configuration."""
        response = client.get("/healthz")
        data = response.json()
        assert "faultInjection" in data
        assert "rate" in data["faultInjection"]
        assert "ping" in data["faultInjection"]
        # Verify types
        assert isinstance(data["faultInjection"]["rate"], (int, float))
        assert isinstance(data["faultInjection"]["ping"], bool)

    def test_healthz_contains_uptime(self):
        """Health endpoint should contain uptimeSeconds."""
        response = client.get("/healthz")
        data = response.json()
        assert "uptimeSeconds" in data
        assert isinstance(data["uptimeSeconds"], (int, float))
        assert data["uptimeSeconds"] >= 0
