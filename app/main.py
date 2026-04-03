from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def is_simulate_failures_enabled() -> bool:
    """Check if SIMULATE_FAILURES env var is set to 'true'."""
    return os.environ.get("SIMULATE_FAILURES", "false").lower() == "true"


@app.get("/ping")
def ping():
    """Health check endpoint. Always returns 200 unless SIMULATE_FAILURES is enabled."""
    if is_simulate_failures_enabled() and int(time.time()) % 3 == 0:
        raise Exception("simulated failure - SIMULATE_FAILURES is enabled")
    return {"pong": True}


@app.get("/fail")
def fail():
    """
    Endpoint for testing failure scenarios.
    When SIMULATE_FAILURES=true, fails deterministically based on time.time() % 3 == 0.
    When SIMULATE_FAILURES=false (default), always returns 200.
    """
    if is_simulate_failures_enabled():
        if int(time.time()) % 3 == 0:
            raise Exception("simulated failure - SIMULATE_FAILURES is enabled")
        return {"status": "ok", "message": "failure simulation enabled but not triggered"}
    return {"status": "ok", "message": "failure simulation disabled"}

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