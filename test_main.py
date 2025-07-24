from main import analyze_sentiment
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_sentiment():
    result = analyze_sentiment("This stock is great!")
    assert result["label"] == "positive"
    assert isinstance(result["score"], float)

def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}