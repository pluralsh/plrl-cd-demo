from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def is_chaos_mode_enabled() -> bool:
    """Check if CHAOS_MODE is enabled via environment variable.

    Returns True if CHAOS_MODE is set to 'true' or '1' (case-insensitive).
    Returns False by default (stable behavior).
    """
    chaos_value = os.environ.get('CHAOS_MODE', '').lower()
    return chaos_value in ('true', '1')


def should_trigger_chaos_error(timestamp: int) -> bool:
    """Determine if chaos error should be triggered based on timestamp.

    This is a pure function to allow deterministic testing.
    """
    return timestamp % 3 == 0


@app.get("/ping")
def ping():
    """Health check endpoint.

    By default, returns stable 200 OK response.
    When CHAOS_MODE=true, intermittently raises 5xx errors (every 3rd second).
    """
    if is_chaos_mode_enabled():
        if should_trigger_chaos_error(int(time.time())):
            raise Exception("unknown internal error")

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