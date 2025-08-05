from main import analyze_sentiment
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_analyze_sentiment():
    result = analyze_sentiment("This stock is great!")
    assert result["label"] == "positive"
    assert isinstance(result["score"], float)

def test_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"])
def test_company_sentiment_route(symbol):
    response = client.get("/sentiment/AAPL")
    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0
    assert "headline" in data[0]
    assert "sentiment" in data[0]