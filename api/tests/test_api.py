from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)

def test_health():
    r=client.get("/health")
    assert r.status_code==200 and r.json()["ok"] is True

def test_integrations_policy():
    data=client.get("/integrations").json()
    assert data["delivery_policy"]["idempotency"] is True
    assert data["delivery_policy"]["retry"]=="exponential"
