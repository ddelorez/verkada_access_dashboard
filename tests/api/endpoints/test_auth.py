from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest # Ensure pytest is imported if specific pytest features are used directly

# Assuming conftest.py is in the parent 'tests' directory and sets up client and db_session
# from ....backend.app.models import user as user_schemas # Adjust if needed for UserCreate schema

# For Pydantic models used in request/response, ensure they are accessible
# This might require adjusting PYTHONPATH or how tests are run.
# Example: from backend.app.models.user import UserCreate, User

# Test for successful registration
def test_register_user_success(client: TestClient, db_session: Session):
    """
    Test successful user registration.
    """
    user_data = {"username": "testuser_success", "password": "testpassword123"}
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data # Ensure password is not returned

    # Verify user is in the database (optional, but good for thoroughness)
    # from backend.app.services import user_service # Direct service call for verification
    # db_user = user_service.get_user_by_username(db_session, username=user_data["username"])
    # assert db_user is not None
    # assert db_user.username == user_data["username"]

# Test for registering a user with an existing username
def test_register_user_existing_username(client: TestClient, db_session: Session):
    """
    Test registration attempt with an already existing username.
    """
    # First, create a user
    user_data_initial = {"username": "existinguser", "password": "testpassword123"}
    client.post("/api/v1/auth/register", json=user_data_initial) # Register the user

    # Attempt to register the same user again
    user_data_duplicate = {"username": "existinguser", "password": "anotherpassword"}
    response = client.post("/api/v1/auth/register", json=user_data_duplicate)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username already registered"

# Test for registration with invalid data (e.g., missing password)
# FastAPI/Pydantic usually handles this with a 422 Unprocessable Entity
def test_register_user_invalid_data_missing_password(client: TestClient):
    """
    Test registration with missing password field.
    Pydantic should return a 422 error.
    """
    user_data = {"username": "testuser_invalid_data"}
    # No password provided
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 422 # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    # Check for specific error message related to 'password' field if desired
    # Example: assert any(err["loc"] == ["body", "password"] for err in data["detail"])

def test_register_user_invalid_data_missing_username(client: TestClient):
    """
    Test registration with missing username field.
    Pydantic should return a 422 error.
    """
    user_data = {"password": "testpassword123"}
    # No username provided
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 422 # Unprocessable Entity
    data = response.json()
    assert "detail" in data
    # Example: assert any(err["loc"] == ["body", "username"] for err in data["detail"])

# Add more tests as needed, e.g., for password complexity if implemented
# Tests for /login/token endpoint

def test_login_for_access_token_success(client: TestClient, db_session: Session):
    """
    Test successful login and token generation.
    """
    # First, register a user
    username = "logintestuser"
    password = "loginpassword123"
    user_data = {"username": username, "password": password}
    response_register = client.post("/api/v1/auth/register", json=user_data)
    assert response_register.status_code == 201

    # Attempt to login
    login_data = {"username": username, "password": password}
    response_login = client.post("/api/v1/auth/login/token", data=login_data) # Use data for form submission
    assert response_login.status_code == 200
    token_data = response_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

def test_login_for_access_token_incorrect_username(client: TestClient):
    """
    Test login attempt with a non-existent username.
    """
    login_data = {"username": "nonexistentuser", "password": "somepassword"}
    response = client.post("/api/v1/auth/login/token", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"

def test_login_for_access_token_incorrect_password(client: TestClient, db_session: Session):
    """
    Test login attempt with correct username but incorrect password.
    """
    # First, register a user
    username = "login_wrong_pw_user"
    password = "correctpassword123"
    user_data = {"username": username, "password": password}
    response_register = client.post("/api/v1/auth/register", json=user_data)
    assert response_register.status_code == 201

    # Attempt to login with incorrect password
    login_data = {"username": username, "password": "wrongpassword"}
    response_login = client.post("/api/v1/auth/login/token", data=login_data)
    assert response_login.status_code == 401
    data = response_login.json()
    assert data["detail"] == "Incorrect username or password"