from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import random

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

# Feature flag for chaos mode (default: false)
CHAOS_MODE = os.environ.get('CHAOS_MODE', 'false').lower() == 'true'


@app.get("/ping")
def ping():
    """
    Ping endpoint.
    When CHAOS_MODE=false: always returns 200 OK.
    When CHAOS_MODE=true: may return 500 errors randomly for chaos testing.
    """
    if CHAOS_MODE:
        # Chaos behavior: randomly fail ~33% of requests
        if random.random() < 0.33:
            raise HTTPException(status_code=500, detail="Chaos mode: simulated internal error")
    return {"pong": True}


@app.get("/healthz")
def healthz():
    """
    Liveness probe endpoint.
    Returns 200 OK when the application is alive.
    This endpoint is never affected by CHAOS_MODE.
    """
    return {"status": "healthy"}


@app.get("/readyz")
def readyz():
    """
    Readiness probe endpoint.
    Returns 200 OK when the application is ready to serve traffic.
    This endpoint is never affected by CHAOS_MODE.
    """
    return {"status": "ready"}

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