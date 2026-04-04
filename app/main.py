from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def is_chaos_enabled() -> bool:
    """Check if chaos testing is enabled via environment variable.

    Evaluates per-request to allow dynamic toggling.
    Only returns True if ENABLE_CHAOS_TESTING is exactly 'true' (case-insensitive).
    """
    return os.getenv("ENABLE_CHAOS_TESTING", "").lower() == "true"


@app.get("/ping")
def test():
    try:
        if is_chaos_enabled():
            if int(time.time()) % 3 == 0:
                raise Exception("chaos testing: simulated internal error")
        return {"pong": True}
    except Exception as e:
        logger.exception("Exception in /ping handler: %s", str(e))
        raise

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