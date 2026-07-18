from abc import ABC, abstractmethod
from typing import List, Optional
from app.infrastructure.persistence.models.user import User

class IUserRepository(ABC):
    """Interface (Port) for User database operations."""

    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user record in the database."""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their unique primary key ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Find a user by their unique email address."""
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        """Retrieve all users in the system."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Delete a user record by ID. Returns True if deleted, False otherwise."""
        pass
