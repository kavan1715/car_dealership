import pytest
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import base class and models
from app.infrastructure.persistence.db import Base
from app.infrastructure.persistence.models.user import User, UserRole
from app.infrastructure.persistence.models.vehicle import Vehicle

# Import exception classes
from app.domain.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
    VehicleNotFoundException,
    OutOfStockException,
    InvalidQuantityException
)

# Import Repositories and Services (TDD RED - these imports will fail initially)
from app.infrastructure.persistence.repositories.user_repository import SqlUserRepository
from app.infrastructure.persistence.repositories.vehicle_repository import SqlVehicleRepository
from app.use_cases.user_service import UserService
from app.use_cases.vehicle_service import VehicleService

# Setup an isolated in-memory SQLite database for testing repos and services
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="db_session")
def fixture_db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

# ==========================================
# REPOSITORY TESTS
# ==========================================

def test_user_repository_create_and_find(db_session):
    repo = SqlUserRepository(db_session)
    user_data = User(name="Jane Doe", email="jane@example.com", hashed_password="hashedpassword")
    
    # Test Create User
    created_user = repo.create(user_data)
    assert created_user.id is not None
    assert created_user.email == "jane@example.com"
    
    # Test Get User by ID
    found_by_id = repo.get_by_id(created_user.id)
    assert found_by_id is not None
    assert found_by_id.name == "Jane Doe"
    
    # Test Get User by Email
    found_by_email = repo.get_by_email("jane@example.com")
    assert found_by_email is not None
    assert found_by_email.id == created_user.id
    
    # Test Get All Users
    all_users = repo.get_all()
    assert len(all_users) == 1
    
    # Test Delete User
    delete_result = repo.delete(created_user.id)
    assert delete_result is True
    assert repo.get_by_id(created_user.id) is None

def test_vehicle_repository_crud(db_session):
    repo = SqlVehicleRepository(db_session)
    vehicle_data = Vehicle(make="Ford", model="Mustang", category="Sports", price=Decimal("45000.00"), quantity=5)
    
    # Test Create Vehicle
    created_vehicle = repo.create(vehicle_data)
    assert created_vehicle.id is not None
    assert created_vehicle.model == "Mustang"
    
    # Test Get Vehicle by ID
    found_vehicle = repo.get_by_id(created_vehicle.id)
    assert found_vehicle is not None
    assert found_vehicle.make == "Ford"
    
    # Test Update Vehicle
    found_vehicle.price = Decimal("48000.00")
    updated_vehicle = repo.update(found_vehicle)
    assert updated_vehicle.price == Decimal("48000.00")
    
    # Test Search Vehicles (by make/model)
    search_make = repo.search(make="ford")
    assert len(search_make) == 1
    
    search_model = repo.search(model="must")
    assert len(search_model) == 1
    
    search_none = repo.search(make="Honda")
    assert len(search_none) == 0

    # Test Delete Vehicle
    delete_result = repo.delete(created_vehicle.id)
    assert delete_result is True
    assert repo.get_by_id(created_vehicle.id) is None

# ==========================================
# SERVICE TESTS
# ==========================================

def test_user_service_duplicate_email(db_session):
    user_repo = SqlUserRepository(db_session)
    user_service = UserService(user_repo)
    
    # Create first user successfully
    user_service.create_user(name="Alice", email="alice@example.com", password="password123")
    
    # Attempt to create second user with duplicate email should raise UserAlreadyExistsException
    with pytest.raises(UserAlreadyExistsException):
        user_service.create_user(name="Alice 2", email="alice@example.com", password="password456")

def test_vehicle_service_validation_rules(db_session):
    vehicle_repo = SqlVehicleRepository(db_session)
    vehicle_service = VehicleService(vehicle_repo)
    
    # Validate make cannot be empty
    with pytest.raises(ValueError, match="Make cannot be empty"):
        vehicle_service.create_vehicle(make="", model="Civic", category="Sedan", price=Decimal("20000"))
        
    # Validate model cannot be empty
    with pytest.raises(ValueError, match="Model cannot be empty"):
        vehicle_service.create_vehicle(make="Honda", model="", category="Sedan", price=Decimal("20000"))
        
    # Validate price cannot be negative
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        vehicle_service.create_vehicle(make="Honda", model="Civic", category="Sedan", price=Decimal("-100"))

def test_vehicle_service_purchase_and_restock_rules(db_session):
    vehicle_repo = SqlVehicleRepository(db_session)
    vehicle_service = VehicleService(vehicle_repo)
    
    # Setup a vehicle
    vehicle = vehicle_service.create_vehicle(make="Toyota", model="RAV4", category="SUV", price=Decimal("30000"), quantity=3)
    
    # Test valid purchase
    purchased = vehicle_service.purchase_vehicle(vehicle.id, 2)
    assert purchased.quantity == 1
    
    # Test out of stock purchase attempt
    with pytest.raises(OutOfStockException):
        vehicle_service.purchase_vehicle(vehicle.id, 5)
        
    # Test invalid purchase quantity (<= 0)
    with pytest.raises(InvalidQuantityException):
        vehicle_service.purchase_vehicle(vehicle.id, -1)
        
    # Test valid restock
    restocked = vehicle_service.restock_vehicle(vehicle.id, 10)
    assert restocked.quantity == 11
    
    # Test invalid restock quantity (<= 0)
    with pytest.raises(InvalidQuantityException):
        vehicle_service.restock_vehicle(vehicle.id, 0)
        
    # Test non-existent vehicle operations
    with pytest.raises(VehicleNotFoundException):
        vehicle_service.purchase_vehicle(999, 1)
        
    with pytest.raises(VehicleNotFoundException):
        vehicle_service.restock_vehicle(999, 1)
