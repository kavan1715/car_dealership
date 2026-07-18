from typing import List, Optional
from sqlalchemy.orm import Session
from app.use_cases.interfaces.user_repository import IUserRepository
from app.infrastructure.persistence.models.user import User

class SqlUserRepository(IUserRepository):
    """SQLAlchemy implementation of the IUserRepository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
