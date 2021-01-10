from fastapi import APIRouter

from db import Mongo
from models.domain.plants import Plant
from models.schemas import ListOfPlants, CreatePlantInput

router = APIRouter()
db = Mongo("plants")


@router.get(path="", response_model=ListOfPlants)
async def get_plants_list():
    plants_list = db.all()
    ps = [Plant(name="Lemon", _id="5ffae88791e1b8e2b3fc3919") for i in range(10)]
    return ListOfPlants(plants=ps)


@router.post(path="", response_model=Plant)
async def add_plant(plant: CreatePlantInput):
    _id = db.insert(**dict(plant))
    raw_plant = db.get_one(_id=_id)
    return Plant(**raw_plant)
