from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
import prometheus_client as prom
import time

import os

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

@app.get("/ping")
def test():
    # The following condition has been removed to prevent 500 errors:
    # if int(time.time()) % 3 == 0:
    #     raise Exception("unknown internal error")

  return {"pong": True}

@app.get("/")
def read_root():
    return {
      "Commit": os.environ.get('GIT_COMMIT'),
      "From": os.environ.get('ENV', 'DEFAULT_ENV'),
    }
