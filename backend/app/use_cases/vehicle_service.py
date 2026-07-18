from typing import List, Optional, Tuple
from decimal import Decimal
from app.use_cases.interfaces.vehicle_repository import IVehicleRepository
from app.infrastructure.persistence.models.vehicle import Vehicle
from app.domain.exceptions import (
    VehicleNotFoundException,
    OutOfStockException,
    InvalidQuantityException
)

class VehicleService:
    """Service layer coordinating business logic for Vehicle operations."""

    def __init__(self, vehicle_repo: IVehicleRepository):
        self.vehicle_repo = vehicle_repo

    def create_vehicle(self, make: str, model: str, category: str, price: Decimal, quantity: int = 0) -> Vehicle:
        # Validations
        if not make or not make.strip():
            raise ValueError("Make cannot be empty.")
        if not model or not model.strip():
            raise ValueError("Model cannot be empty.")
        if not category or not category.strip():
            raise ValueError("Category cannot be empty.")
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if quantity < 0:
            raise ValueError("Quantity must be non-negative.")

        vehicle = Vehicle(
            make=make.strip(),
            model=model.strip(),
            category=category.strip(),
            price=price,
            quantity=quantity
        )
        return self.vehicle_repo.create(vehicle)

    def get_vehicle_by_id(self, vehicle_id: int) -> Vehicle:
        vehicle = self.vehicle_repo.get_by_id(vehicle_id)
        if not vehicle:
            raise VehicleNotFoundException(f"Vehicle with ID {vehicle_id} not found.")
        return vehicle

    def get_all_vehicles(self, page: int = 1, limit: int = 10) -> Tuple[List[Vehicle], int]:
        if page < 1:
            page = 1
        if limit < 1:
            limit = 10
            
        offset = (page - 1) * limit
        vehicles = self.vehicle_repo.get_all(offset=offset, limit=limit)
        total_count = self.vehicle_repo.count()
        return vehicles, total_count

    def search_and_filter_vehicles(
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
        page: int = 1,
        limit: int = 10
    ) -> Tuple[List[Vehicle], int]:
        # Validate price bounds
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValueError("Minimum price cannot be greater than maximum price.")

        # Validate pagination constraints
        if page <= 0:
            raise ValueError("Page must be greater than zero.")
        if limit <= 0:
            raise ValueError("Limit must be greater than zero.")

        # Validate sorting fields
        allowed_sort_columns = [None, "price", "created_at", "make"]
        if sort_by not in allowed_sort_columns:
            raise ValueError("Invalid sort column.")

        allowed_orders = ["asc", "desc"]
        if order not in allowed_orders:
            raise ValueError("Invalid sort order.")

        offset = (page - 1) * limit
        results, total_records = self.vehicle_repo.search_and_filter(
            make=make,
            model=model,
            category=category,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            availability=availability,
            sort_by=sort_by,
            order=order,
            offset=offset,
            limit=limit
        )
        return results, total_records

    def update_vehicle_details(
        self, 
        vehicle_id: int, 
        make: Optional[str] = None, 
        model: Optional[str] = None, 
        category: Optional[str] = None, 
        price: Optional[Decimal] = None,
        quantity: Optional[int] = None
    ) -> Vehicle:
        vehicle = self.get_vehicle_by_id(vehicle_id)

        if make is not None:
            if not make.strip():
                raise ValueError("Make cannot be empty.")
            vehicle.make = make.strip()
            
        if model is not None:
            if not model.strip():
                raise ValueError("Model cannot be empty.")
            vehicle.model = model.strip()
            
        if category is not None:
            if not category.strip():
                raise ValueError("Category cannot be empty.")
            vehicle.category = category.strip()
            
        if price is not None:
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
            vehicle.price = price

        if quantity is not None:
            if quantity < 0:
                raise ValueError("Quantity must be non-negative.")
            vehicle.quantity = quantity

        return self.vehicle_repo.update(vehicle)

    def delete_vehicle(self, vehicle_id: int) -> bool:
        # Verify vehicle exists first
        self.get_vehicle_by_id(vehicle_id)
        return self.vehicle_repo.delete(vehicle_id)

    def search_vehicles(self, make: Optional[str] = None, model: Optional[str] = None) -> List[Vehicle]:
        return self.vehicle_repo.search(make, model)

    def purchase_vehicle(self, vehicle_id: int, quantity: int) -> Vehicle:
        if quantity <= 0:
            raise InvalidQuantityException("Purchase quantity must be greater than zero.")

        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle.quantity < quantity:
            raise OutOfStockException(
                f"Cannot purchase {quantity} units. Only {vehicle.quantity} available in inventory."
            )

        return self.vehicle_repo.purchase(vehicle_id, quantity)

    def restock_vehicle(self, vehicle_id: int, quantity: int) -> Vehicle:
        if quantity <= 0:
            raise InvalidQuantityException("Restock quantity must be greater than zero.")

        # Verify vehicle exists
        self.get_vehicle_by_id(vehicle_id)
        return self.vehicle_repo.restock(vehicle_id, quantity)
