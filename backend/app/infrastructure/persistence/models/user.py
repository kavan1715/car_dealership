import enum
from datetime import datetime
from sqlalchemy import String, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

# Import base class
from app.infrastructure.persistence.db import Base

class UserRole(str, enum.Enum):
    CUSTOMER = "Customer"
    ADMIN = "Admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role_enum"), 
        nullable=False, 
        default=UserRole.CUSTOMER
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now(),
        default=datetime.utcnow
    )
