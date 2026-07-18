from fastapi import APIRouter
from app.infrastructure.web.api_v1.endpoints import auth, vehicles

api_router = APIRouter()

# Mount authentication routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Mount vehicle CRUD routes
api_router.include_router(vehicles.router, prefix="/vehicles", tags=["vehicles"])
