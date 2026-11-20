from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").json() == {"status": "ok"}

def test_synthetic_scam():
    result = client.post("/analyze", json={"text": "Urgent! Account suspended. Click this link and send a gift card: https://example.invalid"})
    assert result.status_code == 200
    assert result.json()["risk_level"] == "high"

def test_benign():
    result = client.post("/analyze", json={"text": "See you for lunch Saturday."})
    assert result.json()["risk_score"] == 0

def test_empty_rejected():
    assert client.post("/analyze", json={"text": ""}).status_code == 422

def test_score_capped():
    text = "urgent gift card password account suspended click this link prize https://example.invalid"
    assert client.post("/analyze", json={"text": text}).json()["risk_score"] <= 100
