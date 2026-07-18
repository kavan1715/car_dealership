import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.infrastructure.persistence.models.user import UserRole

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

class UserRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    password: str
    confirm_password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        trimmed = v.strip().lower()
        if not EMAIL_REGEX.match(trimmed):
            raise ValueError("Invalid email format.")
        return trimmed

    @field_validator("name")
    @classmethod
    def trim_name(cls, v: str) -> str:
        return v.strip()

class UserLoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
