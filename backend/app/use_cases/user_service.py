from typing import List
from app.use_cases.interfaces.user_repository import IUserRepository
from app.infrastructure.persistence.models.user import User, UserRole
from app.domain.exceptions import UserAlreadyExistsException, UserNotFoundException

from app.infrastructure.security.hashing import hash_password

class UserService:
    """Service layer coordinating business logic for User operations."""

    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def create_user(self, name: str, email: str, password: str, role: UserRole = UserRole.CUSTOMER) -> User:
        # Validate data
        if not name or not name.strip():
            raise ValueError("Name cannot be empty.")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty.")
        if not password or not password.strip():
            raise ValueError("Password cannot be empty.")

        # Check duplicate email
        existing_user = self.user_repo.get_by_email(email.strip())
        if existing_user:
            raise UserAlreadyExistsException("User with this email already exists.")

        # Hash password using bcrypt
        hashed_password = hash_password(password)

        user = User(
            name=name.strip(),
            email=email.strip(),
            hashed_password=hashed_password,
            role=role
        )
        return self.user_repo.create(user)

    def get_user_by_id(self, user_id: int) -> User:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found.")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.user_repo.get_by_email(email.strip())
        if not user:
            raise UserNotFoundException(f"User with email '{email}' not found.")
        return user

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all()

    def delete_user(self, user_id: int) -> bool:
        # Verify user exists first
        self.get_user_by_id(user_id)
        return self.user_repo.delete(user_id)

