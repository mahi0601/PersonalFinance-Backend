# tests/integration/test_transactions_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_transactions(mocker):
    mock_transactions = [
        {"id": 1, "amount": 100, "currency": "USD", "type": "debit"},
        {"id": 2, "amount": 200, "currency": "EUR", "type": "credit"}
    ]
    mocker.patch('app.api.transactions.get_user_transactions', return_value=mock_transactions)

    response = client.get("/transactions", headers={"Authorization": "Bearer mocktoken123"})
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["id"] == 1

def test_add_transaction(mocker):
    mock_transaction = {"id": 3, "amount": 150, "currency": "USD", "type": "debit"}
    mocker.patch('app.api.transactions.add_transaction', return_value=mock_transaction)

    response = client.post(
        "/transactions",
        json={"amount": 150, "currency": "USD", "type": "debit"},
        headers={"Authorization": "Bearer mocktoken123"}
    )
    assert response.status_code == 201
    assert response.json()["id"] == 3
    assert response.json()["amount"] == 150
