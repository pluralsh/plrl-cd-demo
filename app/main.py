from fastapi import FastAPI, Request
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import logging
import traceback

import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

# Request counter for deterministic failure
_ping_request_counter = 0

@app.get("/ping")
def test(request: Request):
  """
  Health check endpoint with configurable failure rate.

  Environment variable PING_FAILURE_MODULO controls failure behavior:
  - If unset, empty, non-integer, or <=0: endpoint never intentionally fails
  - If >0: endpoint fails deterministically every Nth request
    Example: PING_FAILURE_MODULO=10 means every 10th request fails

  The failure is deterministic based on an incrementing request counter.
  """
  global _ping_request_counter
  _ping_request_counter += 1

  # Read and validate PING_FAILURE_MODULO environment variable
  ping_failure_modulo_str = os.environ.get('PING_FAILURE_MODULO', '')
  ping_failure_modulo = 0

  try:
    if ping_failure_modulo_str:
      ping_failure_modulo = int(ping_failure_modulo_str)
      if ping_failure_modulo <= 0:
        ping_failure_modulo = 0
  except ValueError:
    # Invalid integer value, disable intentional failures
    ping_failure_modulo = 0

  # Intentional failure based on modulo
  if ping_failure_modulo > 0 and _ping_request_counter % ping_failure_modulo == 0:
    logger.error(
      f"Intentional ping failure triggered: "
      f"request_count={_ping_request_counter}, "
      f"PING_FAILURE_MODULO={ping_failure_modulo}, "
      f"path={request.url.path}, "
      f"method={request.method}"
    )
    raise Exception("intentional test failure")

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