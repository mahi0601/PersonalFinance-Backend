# tests/integration/test_auth_integration.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success(mocker):
    mock_user = {
        "username": "testuser",
        "hashed_password": "hashedpass123"
    }
    mocker.patch('app.api.auth.get_user_by_username', return_value=mock_user)
    mocker.patch('app.core.security.verify_password', return_value=True)
    mocker.patch('app.core.security.create_access_token', return_value="mocktoken123")

    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "plaintext123"}
    )
    assert response.status_code == 200
    assert response.json()["access_token"] == "mocktoken123"

def test_login_failure(mocker):
    mocker.patch('app.api.auth.get_user_by_username', return_value=None)

    response = client.post(
        "/auth/login",
        json={"username": "invaliduser", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_refresh_token_success(mocker):
    mocker.patch('app.api.auth.verify_token', return_value={"sub": "testuser"})
    mocker.patch('app.core.security.create_access_token', return_value="newmocktoken123")

    response = client.post("/auth/refresh", headers={"Authorization": "Bearer mocktoken123"})
    assert response.status_code == 200
    assert response.json()["access_token"] == "newmocktoken123"
