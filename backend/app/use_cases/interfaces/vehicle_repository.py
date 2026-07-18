from abc import ABC, abstractmethod
from typing import List, Optional
from app.infrastructure.persistence.models.vehicle import Vehicle

class IVehicleRepository(ABC):
    """Interface (Port) for Vehicle database operations."""

    @abstractmethod
    def create(self, vehicle: Vehicle) -> Vehicle:
        """Create a new vehicle record in the database."""
        pass

    @abstractmethod
    def get_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        """Find a vehicle by its unique primary key ID."""
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 10) -> List[Vehicle]:
        """Retrieve a paginated slice of vehicles in the inventory."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Get the total count of vehicle records in the database."""
        pass

    @abstractmethod
    def update(self, vehicle: Vehicle) -> Vehicle:
        """Update an existing vehicle record's details."""
        pass

    @abstractmethod
    def delete(self, vehicle_id: int) -> bool:
        """Delete a vehicle record by ID. Returns True if deleted, False otherwise."""
        pass

    @abstractmethod
    def search(self, make: Optional[str] = None, model: Optional[str] = None) -> List[Vehicle]:
        """Search vehicles filtering by make and/or model (case-insensitive partial matches)."""
        pass

    @abstractmethod
    def purchase(self, vehicle_id: int, quantity: int) -> Vehicle:
        """Decrease a vehicle's in-stock count by the specified quantity."""
        pass

    @abstractmethod
    def restock(self, vehicle_id: int, quantity: int) -> Vehicle:
        """Increase a vehicle's in-stock count by the specified quantity."""
        pass
