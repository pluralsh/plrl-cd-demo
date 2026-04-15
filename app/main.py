from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration: demo mode for intentional failures (default: disabled for production safety)
ENABLE_DEMO_FAILURES = os.environ.get("ENABLE_DEMO_FAILURES", "false").lower() in ("true", "1", "yes")

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

@app.get("/ping")
def test():
  if ENABLE_DEMO_FAILURES and int(time.time()) % 3 == 0:
    logger.error("Demo failure triggered", extra={
      "endpoint": "/ping",
      "demo_mode": True,
      "timestamp": int(time.time())
    })
    raise HTTPException(status_code=503, detail="Service temporarily unavailable (demo failure)")

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