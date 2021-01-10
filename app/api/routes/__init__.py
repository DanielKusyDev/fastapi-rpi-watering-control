from fastapi import APIRouter
from app.api.routes import plants

router = APIRouter()

router.include_router(plants.router, tags=["plants"], prefix="/plants")
