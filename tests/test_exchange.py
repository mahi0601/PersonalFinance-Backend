from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_exchange_rate():
    response = client.get("/exchange/USD/", params={"target_currency": "EUR"})
    assert response.status_code == 200
    assert "rate" in response.json()
