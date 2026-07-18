import pytest
from decimal import Decimal
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

# Import base class and models
from app.infrastructure.persistence.db import Base, get_db
from app.infrastructure.persistence.models.user import User, UserRole
from app.infrastructure.persistence.models.vehicle import Vehicle

# Import exceptions
from app.domain.exceptions import VehicleNotFoundException

# Import security and dependencies
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.persistence.repositories.vehicle_repository import SqlVehicleRepository
from app.use_cases.vehicle_service import VehicleService
from app.main import app

# Setup an isolated test database (SQLite) for vehicle endpoint testing
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

@pytest.fixture(name="admin_headers")
def fixture_admin_headers(db_session):
    # Setup Admin user in DB
    admin = User(
        name="Admin User",
        email="admin@example.com",
        hashed_password="some_hashed_password",
        role=UserRole.ADMIN
    )
    db_session.add(admin)
    db_session.commit()
    
    token = create_access_token(data={"user_id": admin.id, "email": admin.email, "role": admin.role.value})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(name="customer_headers")
def fixture_customer_headers(db_session):
    # Setup Customer user in DB
    customer = User(
        name="Customer User",
        email="customer@example.com",
        hashed_password="some_hashed_password",
        role=UserRole.CUSTOMER
    )
    db_session.add(customer)
    db_session.commit()
    
    token = create_access_token(data={"user_id": customer.id, "email": customer.email, "role": customer.role.value})
    return {"Authorization": f"Bearer {token}"}

# ==========================================
# 1. REPOSITORY TESTS (PAGINATION / COUNT)
# ==========================================

def test_repository_pagination_and_counting(db_session):
    repo = SqlVehicleRepository(db_session)
    
    # Assert initial count is 0
    assert repo.count() == 0
    
    # Create 3 vehicles
    for i in range(3):
        repo.create(Vehicle(make="Toyota", model=f"Model {i}", category="SUV", price=Decimal("30000"), quantity=1))
        
    # Assert count is 3
    assert repo.count() == 3
    
    # Test paginated query: page 1 limit 2 (offset 0 limit 2)
    vehicles_page1 = repo.get_all(offset=0, limit=2)
    assert len(vehicles_page1) == 2
    
    # Test paginated query: page 2 limit 2 (offset 2 limit 2)
    vehicles_page2 = repo.get_all(offset=2, limit=2)
    assert len(vehicles_page2) == 1

# ==========================================
# 2. SERVICE VALIDATION TESTS
# ==========================================

def test_service_invalid_price(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    # Verify price must be positive (> 0)
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        service.create_vehicle(make="Toyota", model="Camry", category="Sedan", price=Decimal("0"))
        
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        service.create_vehicle(make="Toyota", model="Camry", category="Sedan", price=Decimal("-50"))

def test_service_invalid_quantity(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    # Verify quantity cannot be negative
    with pytest.raises(ValueError, match="Quantity must be non-negative"):
        service.create_vehicle(make="Toyota", model="Camry", category="Sedan", price=Decimal("20000"), quantity=-1)

def test_service_vehicle_not_found_handling(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    # Verify raises VehicleNotFoundException when retrieving non-existent ID
    with pytest.raises(VehicleNotFoundException):
        service.get_vehicle_by_id(999)
        
    # Verify raises VehicleNotFoundException when updating non-existent ID
    with pytest.raises(VehicleNotFoundException):
        service.update_vehicle_details(999, make="Honda")
        
    # Verify raises VehicleNotFoundException when deleting non-existent ID
    with pytest.raises(VehicleNotFoundException):
        service.delete_vehicle(999)

# ==========================================
# 3. API ROUTE CRUD TESTS
# ==========================================

def test_api_create_vehicle_by_admin(client, admin_headers):
    payload = {
        "make": "Honda",
        "model": "Civic",
        "category": "Sedan",
        "price": 22000.50,
        "quantity": 10
    }
    response = client.post("/api/v1/vehicles", json=payload, headers=admin_headers)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["make"] == "Honda"
    assert data["price"] == "22000.50"
    assert data["quantity"] == 10
    assert "id" in data

def test_api_create_vehicle_unauthorized(client, customer_headers):
    payload = {
        "make": "Honda",
        "model": "Civic",
        "category": "Sedan",
        "price": 22000.50,
        "quantity": 10
    }
    # Customer should be rejected with 403 Forbidden
    response = client.post("/api/v1/vehicles", json=payload, headers=customer_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # Unauthenticated user should be rejected with 401 Unauthorized
    response = client.post("/api/v1/vehicles", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_api_get_vehicles_paginated(client, customer_headers, admin_headers):
    # Setup some database records
    vehicles_data = [
        {"make": "Tesla", "model": "Model S", "category": "Sedan", "price": 90000.00, "quantity": 2},
        {"make": "Tesla", "model": "Model 3", "category": "Sedan", "price": 40000.00, "quantity": 5},
        {"make": "Tesla", "model": "Model X", "category": "SUV", "price": 100000.00, "quantity": 1}
    ]
    for v in vehicles_data:
        client.post("/api/v1/vehicles", json=v, headers=admin_headers)
        
    # Query all vehicles with pagination: page 1 limit 2
    response = client.get("/api/v1/vehicles?page=1&limit=2", headers=customer_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check items list
    assert len(data["items"]) == 2
    assert data["items"][0]["make"] == "Tesla"
    
    # Check metadata properties
    metadata = data["metadata"]
    assert metadata["total_items"] == 3
    assert metadata["page"] == 1
    assert metadata["limit"] == 2
    assert metadata["total_pages"] == 2

def test_api_get_vehicle_by_id(client, customer_headers, admin_headers):
    # Setup vehicle
    payload = {"make": "BMW", "model": "M3", "category": "Coupe", "price": 75000.00, "quantity": 1}
    create_response = client.post("/api/v1/vehicles", json=payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Query by ID
    response = client.get(f"/api/v1/vehicles/{vehicle_id}", headers=customer_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["model"] == "M3"
    assert data["price"] == "75000.00"
    
    # Query non-existent ID
    response = client.get("/api/v1/vehicles/999", headers=customer_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_vehicle(client, admin_headers, customer_headers):
    # Setup vehicle
    payload = {"make": "Nissan", "model": "Altima", "category": "Sedan", "price": 24000.00, "quantity": 3}
    create_response = client.post("/api/v1/vehicles", json=payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Update as Admin
    update_payload = {"make": "Nissan", "model": "Altima", "category": "Sedan", "price": 26500.00, "quantity": 4}
    response = client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_payload, headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["price"] == "26500.00"
    assert response.json()["quantity"] == 4
    
    # Update as Customer (Forbidden)
    response = client.put(f"/api/v1/vehicles/{vehicle_id}", json=update_payload, headers=customer_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_delete_vehicle(client, admin_headers, customer_headers):
    # Setup vehicle
    payload = {"make": "Audi", "model": "A4", "category": "Sedan", "price": 38000.00, "quantity": 1}
    create_response = client.post("/api/v1/vehicles", json=payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Delete as Customer (Forbidden)
    response = client.delete(f"/api/v1/vehicles/{vehicle_id}", headers=customer_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    
    # Delete as Admin (Success)
    response = client.delete(f"/api/v1/vehicles/{vehicle_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Vehicle successfully deleted."
    
    # Try querying deleted vehicle
    response = client.get(f"/api/v1/vehicles/{vehicle_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    # Try deleting again (404)
    response = client.delete(f"/api/v1/vehicles/{vehicle_id}", headers=admin_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
