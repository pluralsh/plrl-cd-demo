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
  """Health check endpoint - always returns 200 OK"""
  return {"ok": True}

@app.get("/ping-chaos")
def ping_chaos():
  """Demo chaos endpoint - intentionally fails based on CHAOS_ENABLED env var"""
  chaos_enabled = os.environ.get('CHAOS_ENABLED', 'true').lower() == 'true'

  if chaos_enabled and int(time.time()) % 3 == 0:
    raise Exception("unknown internal error")

  return {"ok": True, "chaos": chaos_enabled}

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