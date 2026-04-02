from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import random
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

# Environment variables for /ping failure injection (for demo/testing purposes)
# PING_FAIL_ENABLED: Set to "true" to enable intentional 500 errors (default: false)
# PING_FAIL_RATE: Failure rate as percentage 0-100 (default: 33, roughly 1 in 3 requests)
PING_FAIL_ENABLED = os.environ.get("PING_FAIL_ENABLED", "false").lower() == "true"
PING_FAIL_RATE = int(os.environ.get("PING_FAIL_RATE", "33"))

@app.get("/ping")
def ping():
    """Health check endpoint. Returns 200 OK by default.

    When PING_FAIL_ENABLED=true, randomly returns 500 errors at PING_FAIL_RATE percent.
    """
    if PING_FAIL_ENABLED and random.randint(1, 100) <= PING_FAIL_RATE:
        raise Exception("unknown internal error")

    return {"pong": True, "status": "ok"}

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