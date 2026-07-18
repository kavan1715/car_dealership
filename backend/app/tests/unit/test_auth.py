import pytest
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# Import base class and models
from app.infrastructure.persistence.db import Base, get_db
from app.infrastructure.persistence.models.user import User, UserRole

# Import security and auth dependencies (TDD RED - these imports will fail initially)
from app.infrastructure.security.hashing import hash_password, verify_password
from app.infrastructure.security.jwt import create_access_token, decode_access_token
from app.infrastructure.web.dependencies import get_current_user, get_current_admin
from app.main import app

# Setup an isolated test database (SQLite) for auth endpoint testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(name="db_session")
def fixture_db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def fixture_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# ==========================================
# 1. PASSWORD HASHING UTILITY TESTS
# ==========================================

def test_password_hashing():
    raw_password = "secure_password123"
    hashed = hash_password(raw_password)
    
    # Assert hashed is different from raw
    assert hashed != raw_password
    # Verify correct password matches
    assert verify_password(raw_password, hashed) is True
    # Verify incorrect password fails
    assert verify_password("wrong_password", hashed) is False

# ==========================================
# 2. JWT TOKEN UTILITY TESTS
# ==========================================

def test_jwt_generation_and_verification():
    user_data = {"user_id": 1, "email": "test@example.com", "role": "Customer"}
    token = create_access_token(data=user_data, expires_delta=timedelta(minutes=15))
    
    # Decode and verify token
    payload = decode_access_token(token)
    assert payload["user_id"] == 1
    assert payload["email"] == "test@example.com"
    assert payload["role"] == "Customer"

def test_jwt_expired_token():
    user_data = {"user_id": 1, "email": "test@example.com", "role": "Customer"}
    # Create token that expired 5 minutes ago
    token = create_access_token(data=user_data, expires_delta=timedelta(minutes=-5))
    
    # Decoding should raise ValueError or expired token exception (or decode_access_token returns None/raises exception)
    from jwt import ExpiredSignatureError
    with pytest.raises(ExpiredSignatureError):
        decode_access_token(token)

def test_jwt_invalid_token():
    from jwt import InvalidTokenError
    with pytest.raises(InvalidTokenError):
        decode_access_token("this_is_an_invalid_token_string")

# ==========================================
# 3. ENDPOINT REGISTER TESTS
# ==========================================

def test_register_successful(client):
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    payload = {
        "name": "User One",
        "email": "duplicate@example.com",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123"
    }
    # Register first
    client.post("/api/v1/auth/register", json=payload)
    # Register again with same email
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "User with this email already exists."

def test_register_invalid_email(client):
    payload = {
        "name": "John Doe",
        "email": "invalid-email-format",
        "password": "strongpassword123",
        "confirm_password": "strongpassword123"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_register_weak_password(client):
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "short",
        "confirm_password": "short"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Password must be at least 8 characters long" in response.json()["detail"]

def test_register_password_mismatch(client):
    payload = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "strongpassword123",
        "confirm_password": "differentpassword"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Passwords do not match" in response.json()["detail"]

# ==========================================
# 4. ENDPOINT LOGIN TESTS
# ==========================================

def test_login_successful(client):
    # Register first
    register_payload = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123"
    }
    client.post("/api/v1/auth/register", json=register_payload)
    
    # Attempt login
    login_payload = {
        "email": "alice@example.com",
        "password": "securepassword123"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "alice@example.com"
    assert "password" not in data["user"]

def test_login_wrong_password(client):
    register_payload = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "password": "securepassword123",
        "confirm_password": "securepassword123"
    }
    client.post("/api/v1/auth/register", json=register_payload)
    
    # Login with wrong password
    login_payload = {
        "email": "alice@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"

def test_login_unknown_email(client):
    login_payload = {
        "email": "unknown@example.com",
        "password": "somepassword"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Invalid email or password"

# ==========================================
# 5. ROLE-BASED AUTHORIZATION TESTS
# ==========================================

# Temporary protected test endpoints to test dependencies
@app.get("/test/protected/user")
def read_protected_user(current_user: User = Depends(get_current_user)):
    return {"email": current_user.email, "role": current_user.role}

@app.get("/test/protected/admin")
def read_protected_admin(current_admin: User = Depends(get_current_admin)):
    return {"email": current_admin.email, "role": current_admin.role}

def test_authorization_customer_access(client, db_session):
    # Setup Customer user in DB
    customer = User(
        name="Customer User",
        email="customer@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.CUSTOMER
    )
    db_session.add(customer)
    db_session.commit()
    
    token = create_access_token(data={"user_id": customer.id, "email": customer.email, "role": customer.role.value})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Customer should be able to access customer-protected route
    response = client.get("/test/protected/user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["role"] == "Customer"
    
    # Customer should NOT be able to access admin-protected route (403 Forbidden)
    response = client.get("/test/protected/admin", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "Access denied" in response.json()["detail"]

def test_authorization_admin_access(client, db_session):
    # Setup Admin user in DB
    admin = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    
    token = create_access_token(data={"user_id": admin.id, "email": admin.email, "role": admin.role.value})
    headers = {"Authorization": f"Bearer {token}"}
    
    # Admin should be able to access customer-protected route
    response = client.get("/test/protected/user", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["role"] == "Admin"
    
    # Admin should be able to access admin-protected route
    response = client.get("/test/protected/admin", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["role"] == "Admin"

def test_authorization_unauthorized_access(client):
    # Request without token should return 401 Unauthorized
    response = client.get("/test/protected/user")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
