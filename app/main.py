from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time
import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)


def get_chaos_enabled() -> bool:
    """
    Parse CHAOS_ENABLED env var with robust handling.
    Accepts: true/false, 1/0, yes/no (case-insensitive).
    Default: False (chaos disabled).
    """
    value = os.environ.get('CHAOS_ENABLED', 'false').lower().strip()
    return value in ('true', '1', 'yes', 'on')


@app.get("/ping")
def test():
    if get_chaos_enabled():
        # Chaos mode: ~33% of requests fail based on time
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
