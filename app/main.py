from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import logging
import os

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

@app.get("/ping")
def ping(request: Request):
    """
    Health check endpoint that always returns HTTP 200 with {"pong": true}.
    Used for monitoring and alerting.
    """
    logger.info(f"method={request.method} path={request.url.path} status=200")
    return JSONResponse(content={"pong": True}, status_code=200)


@app.get("/healthz")
def healthz():
    """
    Liveness/readiness probe endpoint. Always returns HTTP 200.
    Minimal logging to reduce noise from frequent probe calls.
    """
    return JSONResponse(content={"status": "healthy"}, status_code=200)

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