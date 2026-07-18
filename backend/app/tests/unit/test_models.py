import pytest
from datetime import datetime
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Import our base and the models to test (TDD RED - these imports will fail initially)
from app.infrastructure.persistence.db import Base
from app.infrastructure.persistence.models.user import User, UserRole
from app.infrastructure.persistence.models.vehicle import Vehicle

# Setup an isolated in-memory SQLite database for testing schema constraints
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(name="db_engine")
def fixture_db_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    # Create all tables defined in Base metadata
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(name="db_session")
def fixture_db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

def test_user_table_metadata(db_engine):
    # Verify the table structure and constraints in metadata
    assert "users" in Base.metadata.tables
    table = Base.metadata.tables["users"]
    
    # Assert column existence
    assert "id" in table.columns
    assert "name" in table.columns
    assert "email" in table.columns
    assert "hashed_password" in table.columns
    assert "role" in table.columns
    assert "created_at" in table.columns
    
    # Assert constraints and indexes
    assert table.columns["email"].unique is True
    assert table.columns["email"].nullable is False
    assert table.columns["name"].nullable is False
    assert table.columns["hashed_password"].nullable is False

def test_vehicle_table_metadata(db_engine):
    # Verify the table structure and constraints in metadata
    assert "vehicles" in Base.metadata.tables
    table = Base.metadata.tables["vehicles"]
    
    # Assert column existence
    assert "id" in table.columns
    assert "make" in table.columns
    assert "model" in table.columns
    assert "category" in table.columns
    assert "price" in table.columns
    assert "quantity" in table.columns
    assert "created_at" in table.columns
    assert "updated_at" in table.columns
    
    # Assert type and constraints
    assert table.columns["price"].nullable is False
    assert table.columns["make"].nullable is False
    assert table.columns["model"].nullable is False

def test_user_creation_and_defaults(db_session):
    # Create a user with minimal required fields
    new_user = User(
        name="John Doe",
        email="john@example.com",
        hashed_password="hashedpassword123"
    )
    db_session.add(new_user)
    db_session.commit()
    
    # Query the user back
    queried_user = db_session.query(User).filter_by(email="john@example.com").first()
    
    assert queried_user is not None
    assert queried_user.id is not None
    assert queried_user.name == "John Doe"
    assert queried_user.hashed_password == "hashedpassword123"
    
    # Verify defaults
    assert queried_user.role == UserRole.CUSTOMER
    assert isinstance(queried_user.created_at, datetime)

def test_user_email_uniqueness(db_session):
    # Insert first user
    user1 = User(
        name="User One",
        email="duplicate@example.com",
        hashed_password="password1"
    )
    db_session.add(user1)
    db_session.commit()
    
    # Attempt to insert second user with duplicate email
    user2 = User(
        name="User Two",
        email="duplicate@example.com",
        hashed_password="password2"
    )
    db_session.add(user2)
    
    # Should raise IntegrityError due to uniqueness constraint
    with pytest.raises(IntegrityError):
        db_session.commit()

def test_vehicle_creation_and_defaults(db_session):
    # Create a vehicle with required fields
    new_vehicle = Vehicle(
        make="Toyota",
        model="Camry",
        category="Sedan",
        price=Decimal("25000.50")
    )
    db_session.add(new_vehicle)
    db_session.commit()
    
    # Query vehicle back
    queried_vehicle = db_session.query(Vehicle).filter_by(model="Camry").first()
    
    assert queried_vehicle is not None
    assert queried_vehicle.id is not None
    assert queried_vehicle.make == "Toyota"
    assert queried_vehicle.model == "Camry"
    assert queried_vehicle.category == "Sedan"
    assert queried_vehicle.price == Decimal("25000.50")
    
    # Verify defaults
    assert queried_vehicle.quantity == 0
    assert isinstance(queried_vehicle.created_at, datetime)
    assert isinstance(queried_vehicle.updated_at, datetime)
