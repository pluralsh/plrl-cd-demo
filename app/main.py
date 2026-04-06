from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

# Track application start time for uptime calculation
APP_START_TIME = time.time()

@app.get("/ping")
def test():
  # Only inject failures if PING_FAIL_INJECT env var is explicitly set to "true"
  # This should be OFF by default and only enabled in non-prod environments for testing
  if os.environ.get('PING_FAIL_INJECT', 'false').lower() == 'true':
    if int(time.time()) % 3 == 0:
      raise Exception("unknown internal error")

  uptime_seconds = int(time.time() - APP_START_TIME)
  return {
    "status": "ok",
    "uptime_seconds": uptime_seconds,
    "version": os.environ.get('GIT_COMMIT', 'unknown'),
    "environment": os.environ.get('ENV', 'DEFAULT_ENV')
  }

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