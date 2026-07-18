from fastapi import APIRouter
from app.infrastructure.web.api_v1.endpoints import auth

api_router = APIRouter()

# Mount the auth router under /auth
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
