import time
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)
for i in range(6):
    r = client.get('/ping')
    print(f'attempt:{i+1} status:{r.status_code} body:{r.json()}')
    time.sleep(1)
