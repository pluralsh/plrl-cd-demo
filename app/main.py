from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

ERRORS_ENABLED = os.environ.get("ENABLE_PING_ERRORS", "false").lower() == "true"

@app.get("/ping")
def test():
    if ERRORS_ENABLED and int(time.time()) % 3 == 0:
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
