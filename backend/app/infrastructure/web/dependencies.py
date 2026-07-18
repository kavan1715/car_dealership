from fastapi import Depends
from sqlalchemy.orm import Session

# Import database session generator
from app.infrastructure.persistence.db import get_db

# Import repository interfaces
from app.use_cases.interfaces.user_repository import IUserRepository
from app.use_cases.interfaces.vehicle_repository import IVehicleRepository

# Import repository implementations (Adapters)
from app.infrastructure.persistence.repositories.user_repository import SqlUserRepository
from app.infrastructure.persistence.repositories.vehicle_repository import SqlVehicleRepository

# Import business services (Use Cases)
from app.use_cases.user_service import UserService
from app.use_cases.vehicle_service import VehicleService

def get_user_repository(db: Session = Depends(get_db)) -> IUserRepository:
    """Dependency injector yielding the SqlUserRepository database adapter."""
    return SqlUserRepository(db)

def get_vehicle_repository(db: Session = Depends(get_db)) -> IVehicleRepository:
    """Dependency injector yielding the SqlVehicleRepository database adapter."""
    return SqlVehicleRepository(db)

def get_user_service(user_repo: IUserRepository = Depends(get_user_repository)) -> UserService:
    """Dependency injector yielding the UserService business logic coordinator."""
    return UserService(user_repo)

def get_vehicle_service(vehicle_repo: IVehicleRepository = Depends(get_vehicle_repository)) -> VehicleService:
    """Dependency injector yielding the VehicleService business logic coordinator."""
    return VehicleService(vehicle_repo)
