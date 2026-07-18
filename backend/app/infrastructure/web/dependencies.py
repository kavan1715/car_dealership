from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt

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

# Import security and model structures
from app.infrastructure.security.jwt import decode_access_token
from app.infrastructure.persistence.models.user import User, UserRole
from app.domain.exceptions import UserNotFoundException

# Initialize bearer security scheme
oauth2_scheme = HTTPBearer()

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

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service)
) -> User:
    """FastAPI route dependency to parse JWT token and retrieve the current authenticated User."""
    try:
        payload = decode_access_token(token.credentials)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = user_service.get_user_by_id(user_id)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token"
        )
    except (jwt.InvalidTokenError, UserNotFoundException):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """FastAPI route dependency enforcing role-based access for Admins only."""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required."
        )
    return current_user
