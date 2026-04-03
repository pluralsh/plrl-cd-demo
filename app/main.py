import logging
import os
import random
import uuid
from typing import Callable

from fastapi import FastAPI, HTTPException, Request, Response
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom

# Configure logging with structured format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

# Environment variables for fault injection (default: disabled)
FAULT_INJECT_PING = os.environ.get('FAULT_INJECT_PING', 'false').lower() == 'true'
FAULT_INJECT_RATE = float(os.environ.get('FAULT_INJECT_RATE', '0'))


@app.middleware("http")
async def logging_middleware(request: Request, call_next: Callable) -> Response:
    """Middleware to add request context to logs and handle exceptions."""
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))

    # Add request context for structured logging
    extra = {
        'path': request.url.path,
        'method': request.method,
        'request_id': request_id,
    }

    logger.info(
        f"Request started: path={extra['path']} method={extra['method']} request_id={extra['request_id']}"
    )

    try:
        response = await call_next(request)
        logger.info(
            f"Request completed: path={extra['path']} method={extra['method']} "
            f"request_id={extra['request_id']} status_code={response.status_code}"
        )
        return response
    except Exception as e:
        logger.exception(
            f"Request failed: path={extra['path']} method={extra['method']} "
            f"request_id={extra['request_id']} error={str(e)}"
        )
        raise


@app.get("/ping")
def ping():
    """
    Health check endpoint that returns a simple pong response.

    Fault injection can be enabled via environment variables:
    - FAULT_INJECT_PING: Set to 'true' to enable fault injection (default: false)
    - FAULT_INJECT_RATE: Probability of failure between 0.0 and 1.0 (default: 0)
    """
    if FAULT_INJECT_PING and FAULT_INJECT_RATE > 0:
        if random.random() < FAULT_INJECT_RATE:
            logger.error(
                "Fault injection triggered: simulating internal error on /ping endpoint"
            )
            raise HTTPException(
                status_code=500,
                detail="Simulated internal error (fault injection enabled)"
            )

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
