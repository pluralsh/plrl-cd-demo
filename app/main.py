from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import logging
from typing import Optional

import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default values for fault injection
DEFAULT_FAULT_INJECT_RATE = 0.0
DEFAULT_FAULT_INJECT_PING = True

# Track startup time for uptime calculation
_startup_time = time.time()


def parse_fault_inject_rate(value: Optional[str]) -> float:
    """
    Parse FAULT_INJECT_RATE env var as float.
    - If missing or empty, return default.
    - If invalid (NaN, non-numeric), log warning and return default.
    - Clamp final value into [0, 1] and log if clamping occurred.
    """
    if value is None or value.strip() == "":
        return DEFAULT_FAULT_INJECT_RATE

    try:
        rate = float(value)
        # Check for NaN
        if rate != rate:  # NaN check
            logger.warning(
                f"FAULT_INJECT_RATE value '{value}' is NaN, falling back to default {DEFAULT_FAULT_INJECT_RATE}"
            )
            return DEFAULT_FAULT_INJECT_RATE

        # Clamp to [0, 1]
        if rate < 0:
            logger.warning(
                f"FAULT_INJECT_RATE value {rate} is below 0, clamping to 0"
            )
            return 0.0
        if rate > 1:
            logger.warning(
                f"FAULT_INJECT_RATE value {rate} is above 1, clamping to 1"
            )
            return 1.0

        return rate
    except (ValueError, TypeError):
        logger.warning(
            f"FAULT_INJECT_RATE value '{value}' is invalid, falling back to default {DEFAULT_FAULT_INJECT_RATE}"
        )
        return DEFAULT_FAULT_INJECT_RATE


def parse_fault_inject_ping(value: Optional[str]) -> bool:
    """
    Parse FAULT_INJECT_PING env var as boolean.
    Accepts common forms: true/false, 1/0, yes/no, on/off (case-insensitive).
    If invalid, log warning and return default.
    """
    if value is None or value.strip() == "":
        return DEFAULT_FAULT_INJECT_PING

    normalized = value.strip().lower()

    truthy_values = {"true", "1", "yes", "on"}
    falsy_values = {"false", "0", "no", "off"}

    if normalized in truthy_values:
        return True
    if normalized in falsy_values:
        return False

    logger.warning(
        f"FAULT_INJECT_PING value '{value}' is invalid, falling back to default {DEFAULT_FAULT_INJECT_PING}"
    )
    return DEFAULT_FAULT_INJECT_PING


# Parse environment variables at startup
FAULT_INJECT_RATE = parse_fault_inject_rate(os.environ.get("FAULT_INJECT_RATE"))
FAULT_INJECT_PING = parse_fault_inject_ping(os.environ.get("FAULT_INJECT_PING"))

logger.info(f"Fault injection configured: rate={FAULT_INJECT_RATE}, ping={FAULT_INJECT_PING}")

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


@app.get("/ping")
def test():
    """
    Ping endpoint with optional fault injection.
    If FAULT_INJECT_PING is True, faults may be injected based on FAULT_INJECT_RATE.
    """
    import random

    if FAULT_INJECT_PING and random.random() < FAULT_INJECT_RATE:
        raise Exception("Injected fault for testing")

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


@app.get("/healthz")
def healthz():
    """
    Health check endpoint returning current status and fault injection configuration.
    Returns 200 with JSON body including:
    - status: "ok"
    - faultInjection: { rate: <float>, ping: <bool> }
    - uptimeSeconds: time since startup
    """
    uptime_seconds = round(time.time() - _startup_time, 2)
    return {
        "status": "ok",
        "faultInjection": {
            "rate": FAULT_INJECT_RATE,
            "ping": FAULT_INJECT_PING,
        },
        "uptimeSeconds": uptime_seconds,
    }