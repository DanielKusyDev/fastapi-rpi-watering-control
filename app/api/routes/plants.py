from fastapi import APIRouter

from db import Mongo
from models.domain.plants import Plant
from models.schemas import ListOfPlants, CreatePlantInput

router = APIRouter()
db = Mongo("plants")


@router.post(path="", response_model=Plant)
async def add_plant(plant: CreatePlantInput):
    _id = db.insert(**dict(plant))
    raw_plant = db.get_one(_id=_id)
    return Plant(**raw_plant)
