from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column

# Import base class
from app.infrastructure.persistence.db import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now(),
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, 
        server_default=func.now(),
        onupdate=func.now(),
        default=datetime.utcnow
    )
