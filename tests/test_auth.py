import pytest
from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)

@pytest.fixture
def unique_test_user():
    """Fixture to provide a unique test user payload."""
    username = f"user_{uuid.uuid4().hex[:8]}"  # Generate a unique username
    return {"username": username, "password": "testpass"}

def test_signup(unique_test_user):
    """Test the signup endpoint."""
    response = client.post("/auth/signup/", params=unique_test_user)
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.json()}"
    assert response.json().get("message") == "User created successfully"

def test_login(unique_test_user):
    """Test the login endpoint."""
    # First, sign up the user
    signup_response = client.post("/auth/signup/", params=unique_test_user)
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.json()}"

    # Test login with the same credentials
    login_response = client.post("/auth/login/", params=unique_test_user)
    assert login_response.status_code == 200, f"Unexpected login status: {login_response.json()}"
    assert "access_token" in login_response.json()

def test_duplicate_signup():
    """Test that duplicate signup requests are handled properly."""
    user = {"username": "duplicate_user", "password": "testpass"}

    # First signup
    first_response = client.post("/auth/signup/", params=user)
    if first_response.status_code != 200:
        assert first_response.json().get("detail") == "Username already exists"
    else:
        assert first_response.json().get("message") == "User created successfully"

    # Duplicate signup
    duplicate_response = client.post("/auth/signup/", params=user)
    assert duplicate_response.status_code == 400, f"Unexpected status code: {duplicate_response.json()}"
    assert duplicate_response.json().get("detail") == "Username already exists"
