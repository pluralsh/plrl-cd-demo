from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import random
import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def _get_ping_fail_rate() -> float:
    """
    Read and validate PING_FAIL_RATE env var.
    Returns a float clamped to [0.0, 1.0], defaulting to 0.0 if missing or invalid.
    """
    raw = os.environ.get("PING_FAIL_RATE", "0.0")
    try:
        rate = float(raw)
    except (ValueError, TypeError):
        return 0.0
    # Clamp to valid range
    return max(0.0, min(1.0, rate))


def _default_rng() -> float:
    """Default random number generator, returns float in [0.0, 1.0)."""
    return random.random()


# Allows injection of a custom RNG function for deterministic testing
_rng_func = _default_rng


def set_rng_func(func):
    """Set a custom RNG function (for testing). Pass None to reset to default."""
    global _rng_func
    _rng_func = func if func is not None else _default_rng


@app.get("/ping")
def ping():
    """
    Health check endpoint.

    By default, always returns HTTP 200 with {"pong": True}.

    When PING_FAIL_RATE env var is set (float 0.0-1.0), enables chaos mode:
    - 0.0 = always succeed (default)
    - 1.0 = always fail
    - 0.5 = 50% chance of failure

    Failures return HTTP 500 with a clear error message.
    """
    fail_rate = _get_ping_fail_rate()

    if fail_rate > 0 and _rng_func() < fail_rate:
        raise HTTPException(
            status_code=500,
            detail="Chaos mode failure: PING_FAIL_RATE triggered simulated error"
        )

    return {"pong": True}

@app.get("/hello")
def hello():
  return {"hello": "world!"}

@app.get("/world")
def world():
  return {"world": "hello!"}

@app.get("/")
def read_root():
    return {
      "Commit": os.environ.get('GIT_COMMIT'),
      "From": os.environ.get('ENV', 'DEFAULT_ENV'),
    }