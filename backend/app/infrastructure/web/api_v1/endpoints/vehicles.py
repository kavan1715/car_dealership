from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
import math

from app.infrastructure.web.dependencies import (
    get_vehicle_service,
    get_current_user,
    get_current_admin
)
from app.use_cases.vehicle_service import VehicleService
from app.infrastructure.persistence.models.user import User
from app.domain.exceptions import VehicleNotFoundException
from app.infrastructure.web.schemas.vehicle import (
    VehicleCreate,
    VehicleUpdate,
    VehicleResponse,
    VehicleListResponse,
    PaginationMetadata
)

router = APIRouter()

@router.post("", response_model=VehicleResponse, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    payload: VehicleCreate,
    current_admin: User = Depends(get_current_admin),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        vehicle = vehicle_service.create_vehicle(
            make=payload.make,
            model=payload.model,
            category=payload.category,
            price=payload.price,
            quantity=payload.quantity
        )
        return vehicle
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("", response_model=VehicleListResponse)
def get_vehicles(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    vehicles, total_items = vehicle_service.get_all_vehicles(page=page, limit=limit)
    total_pages = math.ceil(total_items / limit) if total_items > 0 else 0
    
    metadata = PaginationMetadata(
        total_items=total_items,
        page=page,
        limit=limit,
        total_pages=total_pages
    )
    return VehicleListResponse(items=vehicles, metadata=metadata)

@router.get("/{id}", response_model=VehicleResponse)
def get_vehicle_by_id(
    id: int,
    current_user: User = Depends(get_current_user),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        vehicle = vehicle_service.get_vehicle_by_id(id)
        return vehicle
    except VehicleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.put("/{id}", response_model=VehicleResponse)
def update_vehicle(
    id: int,
    payload: VehicleUpdate,
    current_admin: User = Depends(get_current_admin),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        vehicle = vehicle_service.update_vehicle_details(
            vehicle_id=id,
            make=payload.make,
            model=payload.model,
            category=payload.category,
            price=payload.price,
            quantity=payload.quantity
        )
        return vehicle
    except VehicleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_vehicle(
    id: int,
    current_admin: User = Depends(get_current_admin),
    vehicle_service: VehicleService = Depends(get_vehicle_service)
):
    try:
        vehicle_service.delete_vehicle(id)
        return {"message": "Vehicle successfully deleted."}
    except VehicleNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
