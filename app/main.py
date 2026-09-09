from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional
import prometheus_client as prom
import time
import os

from .database import init_db, get_db, Item, POSTGRES_URL

app = FastAPI()
Instrumentator().instrument(app)

prom.start_http_server(9090)

init_db()


class ItemPayload(BaseModel):
    name: str
    description: Optional[str] = None


def db_required(db: Session = Depends(get_db)):
    if db is None:
        raise HTTPException(status_code=503, detail="Database not configured (POSTGRES_URL not set)")
    return db


@app.get("/ping")
def test():
    if os.environ.get("PING_FAIL_ENABLED") == "true" and int(time.time()) % 3 == 0:
        raise Exception("unknown internal error")
    return {"pong": True}


@app.get("/hello")
def hello():
    return {"hello": "world!"}


@app.get("/world")
def world():
    return {"world": "hello!"}


@app.get("/user")
def user():
    return {"user:": "bob"}


@app.get("/")
def read_root():
    return {
        "Commit": os.environ.get('GIT_COMMIT'),
        "From": os.environ.get('ENV', 'DEFAULT_ENV'),
        "DB": "connected" if POSTGRES_URL else "not configured",
    }


# --- Items CRUD ---

@app.get("/items")
def list_items(db: Session = Depends(db_required)):
    return db.query(Item).all()


@app.get("/items/{item_id}")
def get_item(item_id: int, db: Session = Depends(db_required)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items", status_code=201)
def create_item(payload: ItemPayload, db: Session = Depends(db_required)):
    item = Item(name=payload.name, description=payload.description)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, payload: ItemPayload, db: Session = Depends(db_required)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = payload.name
    item.description = payload.description
    db.commit()
    db.refresh(item)
    return item


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(db_required)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return JSONResponse(status_code=204, content=None)
