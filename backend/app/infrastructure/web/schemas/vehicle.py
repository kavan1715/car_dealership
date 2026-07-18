from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

class VehicleCreate(BaseModel):
    make: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1)
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)

    @field_validator("make", "model", "category")
    @classmethod
    def trim_strings(cls, v: str) -> str:
        return v.strip()

class VehicleUpdate(BaseModel):
    make: Optional[str] = Field(default=None, min_length=1)
    model: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, min_length=1)
    price: Optional[Decimal] = Field(default=None, gt=0)
    quantity: Optional[int] = Field(default=None, ge=0)

    @field_validator("make", "model", "category")
    @classmethod
    def trim_optional_strings(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return v.strip()
        return v

class VehicleResponse(BaseModel):
    id: int
    make: str
    model: str
    category: str
    price: Decimal
    quantity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginationMetadata(BaseModel):
    total_items: int
    page: int
    limit: int
    total_pages: int

class VehicleListResponse(BaseModel):
    items: List[VehicleResponse]
    metadata: PaginationMetadata
