# tests/integration/test_exchange_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_exchange_rates(mocker):
    mock_rates = {"USD": 1.0, "EUR": 0.85, "JPY": 110.0}
    mocker.patch('app.api.exchange.get_all_exchange_rates', return_value=mock_rates)

    response = client.get("/exchange/rates")
    assert response.status_code == 200
    assert response.json()["USD"] == 1.0
    assert response.json()["EUR"] == 0.85
    assert response.json()["JPY"] == 110.0

def test_currency_conversion(mocker):
    mocker.patch('app.api.exchange.get_exchange_rate', return_value=1.2)

    response = client.post(
        "/exchange/convert",
        json={"amount": 100, "from_currency": "USD", "to_currency": "EUR"}
    )
    assert response.status_code == 200
    assert response.json()["converted_amount"] == 120.0
