from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def _parse_bool_env(name: str, default: bool = False) -> bool:
    """Parse boolean environment variable. Accepts true/1/yes (case-insensitive)."""
    value = os.environ.get(name, "").lower()
    if value in ("true", "1", "yes"):
        return True
    if value in ("false", "0", "no"):
        return False
    return default


@app.get("/ping")
def ping():
    """
    Health check endpoint.

    When CHAOS_MODE is disabled (default): always returns HTTP 200 with "ok".
    When CHAOS_MODE is enabled: simulates intermittent failures (500 errors)
    for chaos testing purposes.
    """
    chaos_mode = _parse_bool_env("CHAOS_MODE", default=False)

    if not chaos_mode:
        # Normal mode: always healthy
        return {"status": "ok"}

    # Chaos mode: simulate intermittent failures for testing
    if int(time.time()) % 3 == 0:
        raise HTTPException(status_code=500, detail="chaos: simulated internal error")

    return {"status": "ok", "chaos_mode": True}

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