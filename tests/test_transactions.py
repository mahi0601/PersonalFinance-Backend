from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction():
    response = client.post("/transactions/", json={
        "user_id": 1,
        "amount": 100.0,
        "category": "Food",
        "description": "Groceries"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Transaction created successfully"
