from typing import List, Optional, Tuple
from decimal import Decimal
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.use_cases.interfaces.vehicle_repository import IVehicleRepository
from app.infrastructure.persistence.models.vehicle import Vehicle

class SqlVehicleRepository(IVehicleRepository):
    """SQLAlchemy implementation of the IVehicleRepository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, vehicle: Vehicle) -> Vehicle:
        try:
            self.db.add(vehicle)
            self.db.commit()
            self.db.refresh(vehicle)
            return vehicle
        except Exception:
            self.db.rollback()
            raise

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_all(self, offset: int = 0, limit: int = 10) -> List[Vehicle]:
        return self.db.query(Vehicle).offset(offset).limit(limit).all()

    def count(self) -> int:
        return self.db.query(Vehicle).count()

    def update(self, vehicle: Vehicle) -> Vehicle:
        try:
            self.db.commit()
            self.db.refresh(vehicle)
            return vehicle
        except Exception:
            self.db.rollback()
            raise

    def delete(self, vehicle_id: int) -> bool:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            try:
                self.db.delete(vehicle)
                self.db.commit()
                return True
            except Exception:
                self.db.rollback()
                raise
        return False

    def search(self, make: Optional[str] = None, model: Optional[str] = None) -> List[Vehicle]:
      query = self.db.query(Vehicle)
      if make:
          query = query.filter((Vehicle.make.ilike(f"%{make}%")) | (Vehicle.model.ilike(f"%{make}%")))
      if model:
          query = query.filter((Vehicle.make.ilike(f"%{model}%")) | (Vehicle.model.ilike(f"%{model}%")))
      return query.all()

    def search_and_filter(
        self,
        make: Optional[str] = None,
        model: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[Decimal] = None,
        max_price: Optional[Decimal] = None,
        min_quantity: Optional[int] = None,
        availability: Optional[bool] = None,
        sort_by: Optional[str] = None,
        order: str = "asc",
        offset: int = 0,
        limit: int = 10
    ) -> Tuple[List[Vehicle], int]:
        query = self.db.query(Vehicle)

        if make:
            query = query.filter((Vehicle.make.ilike(f"%{make}%")) | (Vehicle.model.ilike(f"%{make}%")))
        if model:
            query = query.filter((Vehicle.make.ilike(f"%{model}%")) | (Vehicle.model.ilike(f"%{model}%")))
        if category:
            query = query.filter(Vehicle.category == category)
        if min_price is not None:
            query = query.filter(Vehicle.price >= min_price)
        if max_price is not None:
            query = query.filter(Vehicle.price <= max_price)
        if min_quantity is not None:
            query = query.filter(Vehicle.quantity >= min_quantity)
        if availability is not None:
            if availability:
                query = query.filter(Vehicle.quantity > 0)
            else:
                query = query.filter(Vehicle.quantity == 0)

        # Count total matches before applying pagination slice limits
        total_count = query.count()

        # Sorting logic
        if sort_by:
            column = getattr(Vehicle, sort_by, None)
            if column is not None:
                if order == "desc":
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column.asc())
        else:
            # Default sorting to insertion order
            query = query.order_by(Vehicle.id.asc())

        # Pagination slicing
        results = query.offset(offset).limit(limit).all()
        return results, total_count

    def purchase(self, vehicle_id: int, quantity: int) -> Vehicle:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            try:
                vehicle.quantity -= quantity
                self.db.commit()
                self.db.refresh(vehicle)
            except Exception:
                self.db.rollback()
                raise
        return vehicle

    def restock(self, vehicle_id: int, quantity: int) -> Vehicle:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            try:
                vehicle.quantity += quantity
                self.db.commit()
                self.db.refresh(vehicle)
            except Exception:
                self.db.rollback()
                raise
        return vehicle
