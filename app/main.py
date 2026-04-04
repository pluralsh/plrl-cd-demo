from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def is_chaos_mode_enabled() -> bool:
    """Check if chaos mode is enabled via CHAOS_MODE env var."""
    return os.environ.get('CHAOS_MODE', 'false').lower() == 'true'


@app.get("/healthz", response_class=PlainTextResponse)
def healthz():
    """Stable health endpoint that always returns 200 OK. Used for probes."""
    return "ok"


@app.get("/ping")
def test():
    """
    Ping endpoint. By default returns success.
    When CHAOS_MODE=true, injects failures ~33% of the time for chaos testing.
    """
    if is_chaos_mode_enabled() and int(time.time()) % 3 == 0:
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