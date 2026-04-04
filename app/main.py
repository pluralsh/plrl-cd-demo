from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import logging

import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler that logs full stack traces and returns HTTP 500.
    Includes request context (method, URL, client) in log output.
    """
    logger.exception(
        "Unhandled exception occurred",
        extra={
            "request_method": request.method,
            "request_url": str(request.url),
            "client_host": request.client.host if request.client else None,
        }
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


@app.get("/ping")
def ping():
    """Health check endpoint - always returns HTTP 200 with pong response."""
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