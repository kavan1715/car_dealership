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
from app.domain.exceptions import (
    OutOfStockException,
    VehicleNotFoundException,
    InvalidQuantityException
)

# Import security and repositories
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.persistence.repositories.vehicle_repository import SqlVehicleRepository
from app.use_cases.vehicle_service import VehicleService
from app.main import app

# Setup an isolated test database (SQLite) for inventory testing
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
    admin = User(name="Admin User", email="admin@example.com", hashed_password="some_hashed_password", role=UserRole.ADMIN)
    db_session.add(admin)
    db_session.commit()
    
    token = create_access_token(data={"user_id": admin.id, "email": admin.email, "role": admin.role.value})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(name="customer_headers")
def fixture_customer_headers(db_session):
    customer = User(name="Customer User", email="customer@example.com", hashed_password="some_hashed_password", role=UserRole.CUSTOMER)
    db_session.add(customer)
    db_session.commit()
    
    token = create_access_token(data={"user_id": customer.id, "email": customer.email, "role": customer.role.value})
    return {"Authorization": f"Bearer {token}"}

# ==========================================
# 1. REPOSITORY TESTS
# ==========================================

def test_repo_purchase_vehicle(db_session):
    repo = SqlVehicleRepository(db_session)
    vehicle = Vehicle(make="Toyota", model="RAV4", category="SUV", price=Decimal("30000"), quantity=2)
    repo.create(vehicle)
    
    # Run purchase operation decreasing stock by 1
    repo.purchase(vehicle.id, 1)
    db_session.refresh(vehicle)
    assert vehicle.quantity == 1

def test_repo_restock_vehicle(db_session):
    repo = SqlVehicleRepository(db_session)
    vehicle = Vehicle(make="Toyota", model="RAV4", category="SUV", price=Decimal("30000"), quantity=2)
    repo.create(vehicle)
    
    # Run restock operation increasing stock by 5
    repo.restock(vehicle.id, 5)
    db_session.refresh(vehicle)
    assert vehicle.quantity == 7

def test_repo_update_quantity(db_session):
    repo = SqlVehicleRepository(db_session)
    vehicle = Vehicle(make="Toyota", model="RAV4", category="SUV", price=Decimal("30000"), quantity=2)
    repo.create(vehicle)
    
    # Explicitly update vehicle quantity
    vehicle.quantity = 15
    repo.update(vehicle)
    
    found = repo.get_by_id(vehicle.id)
    assert found.quantity == 15

# ==========================================
# 2. SERVICE TESTS
# ==========================================

def test_service_out_of_stock_purchase(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    vehicle = service.create_vehicle(make="Honda", model="Civic", category="Sedan", price=Decimal("20000"), quantity=0)
    
    with pytest.raises(OutOfStockException):
        service.purchase_vehicle(vehicle.id, 1)

def test_service_invalid_quantity_restock(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    vehicle = service.create_vehicle(make="Honda", model="Civic", category="Sedan", price=Decimal("20000"), quantity=2)
    
    with pytest.raises(InvalidQuantityException):
        service.restock_vehicle(vehicle.id, 0)
        
    with pytest.raises(InvalidQuantityException):
        service.restock_vehicle(vehicle.id, -5)

def test_service_inventory_vehicle_not_found(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    with pytest.raises(VehicleNotFoundException):
        service.purchase_vehicle(999, 1)
        
    with pytest.raises(VehicleNotFoundException):
        service.restock_vehicle(999, 5)

def test_service_successful_purchase(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    vehicle = service.create_vehicle(make="Honda", model="Civic", category="Sedan", price=Decimal("20000"), quantity=3)
    
    updated = service.purchase_vehicle(vehicle.id, 1)
    assert updated.quantity == 2

def test_service_successful_restock(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    vehicle = service.create_vehicle(make="Honda", model="Civic", category="Sedan", price=Decimal("20000"), quantity=3)
    
    updated = service.restock_vehicle(vehicle.id, 10)
    assert updated.quantity == 13

# ==========================================
# 3. API ROUTE TESTS
# ==========================================

def test_api_purchase_success(client, customer_headers, admin_headers):
    # Setup vehicle using Admin headers
    setup_payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 20000.00, "quantity": 1}
    create_response = client.post("/api/v1/vehicles", json=setup_payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Customer purchases the vehicle
    response = client.post(f"/api/v1/vehicles/{vehicle_id}/purchase", headers=customer_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 0

def test_api_purchase_out_of_stock(client, customer_headers, admin_headers):
    # Setup out of stock vehicle
    setup_payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 20000.00, "quantity": 0}
    create_response = client.post("/api/v1/vehicles", json=setup_payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Customer attempts to purchase out of stock vehicle
    response = client.post(f"/api/v1/vehicles/{vehicle_id}/purchase", headers=customer_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Out of Stock"

def test_api_purchase_unauthorized(client):
    response = client.post("/api/v1/vehicles/1/purchase")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_api_restock_success(client, admin_headers):
    # Setup vehicle
    setup_payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 20000.00, "quantity": 2}
    create_response = client.post("/api/v1/vehicles", json=setup_payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Admin restocks with 5 units
    restock_payload = {"quantity": 5}
    response = client.post(f"/api/v1/vehicles/{vehicle_id}/restock", json=restock_payload, headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["quantity"] == 7

def test_api_restock_unauthorized(client, customer_headers, admin_headers):
    setup_payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 20000.00, "quantity": 2}
    create_response = client.post("/api/v1/vehicles", json=setup_payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Customer attempts to restock (Forbidden)
    restock_payload = {"quantity": 5}
    response = client.post(f"/api/v1/vehicles/{vehicle_id}/restock", json=restock_payload, headers=customer_headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_api_restock_invalid_quantity(client, admin_headers):
    setup_payload = {"make": "Honda", "model": "Civic", "category": "Sedan", "price": 20000.00, "quantity": 2}
    create_response = client.post("/api/v1/vehicles", json=setup_payload, headers=admin_headers)
    vehicle_id = create_response.json()["id"]
    
    # Restock with negative quantity (returns 422 because schema enforces gt=0, or 400 Bad Request)
    # Pydantic schema validation returns 422, which is correct and handled by FastAPI. We assert 422 or 400.
    response = client.post(f"/api/v1/vehicles/{vehicle_id}/restock", json={"quantity": -1}, headers=admin_headers)
    assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_422_UNPROCESSABLE_ENTITY]
