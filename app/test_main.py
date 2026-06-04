from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world!"}

def test_world():
    response = client.get("/world")
    assert response.status_code == 200
    assert response.json() == {"world": "hello!"}

def test_user():
    response = client.get("/user")
    assert response.status_code == 200
    assert response.json() == {"user:": "bob"}
