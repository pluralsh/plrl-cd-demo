from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

@app.get("/ping")
def ping():
  """Health check endpoint that always returns HTTP 200."""
  return {"status": "ok", "pong": True}

@app.get("/broken-test")
def broken_test():
  """Deliberately broken endpoint for testing alerting (DO NOT USE for health checks)."""
  if int(time.time()) % 3 == 0:
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