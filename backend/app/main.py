from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.infrastructure.persistence.db import get_db, Base, engine
from app.infrastructure.web.api_v1.router import api_router
# Import models to ensure registry on Base before creation
from app.infrastructure.persistence.models.user import User
from app.infrastructure.persistence.models.vehicle import Vehicle

# Create all database tables automatically on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Car Dealership API",
    description="Enterprise-grade Clean Architecture Backend API for Car Dealership",
    version="1.0.0"
)

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Car Dealership API"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        # Execute a simple query to verify database connectivity
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
