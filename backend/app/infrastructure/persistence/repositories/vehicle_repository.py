from typing import List, Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.use_cases.interfaces.vehicle_repository import IVehicleRepository
from app.infrastructure.persistence.models.vehicle import Vehicle

class SqlVehicleRepository(IVehicleRepository):
    """SQLAlchemy implementation of the IVehicleRepository."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, vehicle: Vehicle) -> Vehicle:
        self.db.add(vehicle)
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    def get_all(self) -> List[Vehicle]:
        return self.db.query(Vehicle).all()

    def update(self, vehicle: Vehicle) -> Vehicle:
        self.db.commit()
        self.db.refresh(vehicle)
        return vehicle

    def delete(self, vehicle_id: int) -> bool:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            self.db.delete(vehicle)
            self.db.commit()
            return True
        return False

    def search(self, make: Optional[str] = None, model: Optional[str] = None) -> List[Vehicle]:
        query = self.db.query(Vehicle)
        
        # Apply case-insensitive partial match queries for make and model
        if make:
            query = query.filter(Vehicle.make.ilike(f"%{make}%"))
        if model:
            query = query.filter(Vehicle.model.ilike(f"%{model}%"))
            
        return query.all()

    def purchase(self, vehicle_id: int, quantity: int) -> Vehicle:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            vehicle.quantity -= quantity
            self.db.commit()
            self.db.refresh(vehicle)
        return vehicle

    def restock(self, vehicle_id: int, quantity: int) -> Vehicle:
        vehicle = self.get_by_id(vehicle_id)
        if vehicle:
            vehicle.quantity += quantity
            self.db.commit()
            self.db.refresh(vehicle)
        return vehicle
