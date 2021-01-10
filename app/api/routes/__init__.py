from fastapi import APIRouter
from app.api.routes import plants, sensors

router = APIRouter()

router.include_router(plants.router, tags=["plants"], prefix="/plants")
router.include_router(sensors.router, tags=["sensors"], prefix="/sensors")
