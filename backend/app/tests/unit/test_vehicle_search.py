import pytest
from datetime import datetime, timedelta
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

# Import security and repositories
from app.infrastructure.security.jwt import create_access_token
from app.infrastructure.persistence.repositories.vehicle_repository import SqlVehicleRepository
from app.use_cases.vehicle_service import VehicleService
from app.main import app

# Setup an isolated test database (SQLite) for search testing
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

@pytest.fixture(name="user_headers")
def fixture_user_headers(db_session):
    user = User(
        name="Test User",
        email="test@example.com",
        hashed_password="some_hashed_password",
        role=UserRole.CUSTOMER
    )
    db_session.add(user)
    db_session.commit()
    
    token = create_access_token(data={"user_id": user.id, "email": user.email, "role": user.role.value})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(name="seed_vehicles")
def fixture_seed_vehicles(db_session):
    repo = SqlVehicleRepository(db_session)
    # Seed 5 vehicles for filter, search, pagination, and sort validations
    v1 = Vehicle(make="BMW", model="X5", category="SUV", price=Decimal("60000.00"), quantity=2, created_at=datetime.utcnow() - timedelta(days=5))
    v2 = Vehicle(make="BMW", model="330i", category="Sedan", price=Decimal("45000.00"), quantity=4, created_at=datetime.utcnow() - timedelta(days=3))
    v3 = Vehicle(make="Audi", model="Q7", category="SUV", price=Decimal("70000.00"), quantity=0, created_at=datetime.utcnow() - timedelta(days=1))
    v4 = Vehicle(make="Toyota", model="RAV4", category="SUV", price=Decimal("30000.00"), quantity=10, created_at=datetime.utcnow() - timedelta(days=4))
    v5 = Vehicle(make="Toyota", model="Corolla", category="Sedan", price=Decimal("20000.00"), quantity=1, created_at=datetime.utcnow() - timedelta(days=2))
    
    repo.create(v1)
    repo.create(v2)
    repo.create(v3)
    repo.create(v4)
    repo.create(v5)
    return [v1, v2, v3, v4, v5]

# ==========================================
# 1. REPOSITORY TESTS
# ==========================================

def test_repo_search_by_make(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # Search "bmw" (case-insensitive)
    results, count = repo.search_and_filter(make="bmw")
    assert count == 2
    assert len(results) == 2
    assert all(v.make == "BMW" for v in results)

def test_repo_search_by_model(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    results, count = repo.search_and_filter(model="cor")
    assert count == 1
    assert results[0].model == "Corolla"

def test_repo_filter_by_category(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    results, count = repo.search_and_filter(category="SUV")
    assert count == 3
    assert len(results) == 3

def test_repo_filter_by_price_range(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # Between 25000 and 50000
    results, count = repo.search_and_filter(min_price=Decimal("25000"), max_price=Decimal("50000"))
    assert count == 2  # Toyota RAV4 (30000), BMW 330i (45000)
    assert len(results) == 2

def test_repo_filter_by_availability_and_quantity(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # Availability = True (quantity > 0) -> filters out Audi Q7 (quantity = 0)
    results, count = repo.search_and_filter(availability=True)
    assert count == 4
    assert len(results) == 4
    assert all(v.quantity > 0 for v in results)
    
    # Minimum quantity 4 -> RAV4 (10), 330i (4)
    results, count = repo.search_and_filter(min_quantity=4)
    assert count == 2

def test_repo_combined_filters(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # BMW + SUV + Available
    results, count = repo.search_and_filter(make="BMW", category="SUV", availability=True)
    assert count == 1
    assert results[0].model == "X5"

def test_repo_sorting(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # Sort by price descending
    results, count = repo.search_and_filter(sort_by="price", order="desc")
    assert results[0].price == Decimal("70000.00") # Audi Q7
    assert results[-1].price == Decimal("20000.00") # Toyota Corolla
    
    # Sort by make ascending (alphabetical)
    results, count = repo.search_and_filter(sort_by="make", order="asc")
    assert results[0].make == "Audi"
    assert results[-1].make == "Toyota"

def test_repo_pagination(db_session, seed_vehicles):
    repo = SqlVehicleRepository(db_session)
    # Page 1 limit 2 (offset 0 limit 2)
    results, count = repo.search_and_filter(offset=0, limit=2)
    assert count == 5
    assert len(results) == 2

# ==========================================
# 2. SERVICE VALIDATION TESTS
# ==========================================

def test_service_invalid_price_range(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    # Min price > max price raises ValueError
    with pytest.raises(ValueError, match="Minimum price cannot be greater than maximum price"):
        service.search_and_filter_vehicles(min_price=Decimal("1000"), max_price=Decimal("500"))

def test_service_invalid_pagination(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    with pytest.raises(ValueError, match="Page must be greater than zero"):
        service.search_and_filter_vehicles(page=0)
        
    with pytest.raises(ValueError, match="Limit must be greater than zero"):
        service.search_and_filter_vehicles(limit=0)

def test_service_invalid_sorting(db_session):
    repo = SqlVehicleRepository(db_session)
    service = VehicleService(repo)
    
    # Invalid sort_by column
    with pytest.raises(ValueError, match="Invalid sort column"):
        service.search_and_filter_vehicles(sort_by="invalid_col")
        
    # Invalid sort order
    with pytest.raises(ValueError, match="Invalid sort order"):
        service.search_and_filter_vehicles(sort_by="price", order="invalid_order")

# ==========================================
# 3. API ROUTE SEARCH & FILTER TESTS
# ==========================================

def test_api_search_and_filter_successful(client, user_headers, db_session, seed_vehicles):
    # Search BMW SUVs that are in stock
    response = client.get("/api/v1/vehicles/search?make=BMW&category=SUV&availability=true", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["total_records"] == 1
    assert data["total_pages"] == 1
    assert data["current_page"] == 1
    assert data["page_size"] == 10
    assert len(data["results"]) == 1
    assert data["results"][0]["model"] == "X5"

def test_api_search_unauthorized(client):
    response = client.get("/api/v1/vehicles/search?make=BMW")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_api_search_empty_results(client, user_headers, db_session):
    # Query database with no seeded records
    response = client.get("/api/v1/vehicles/search?make=NonExistent", headers=user_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_records"] == 0
    assert len(data["results"]) == 0

def test_api_search_validation_errors(client, user_headers, db_session, seed_vehicles):
    # Invalid price range
    response = client.get("/api/v1/vehicles/search?minimum_price=5000&maximum_price=1000", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Minimum price cannot be greater than maximum price" in response.json()["detail"]
    
    # Invalid sort column
    response = client.get("/api/v1/vehicles/search?sort_by=invalid_field", headers=user_headers)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid sort column" in response.json()["detail"]
