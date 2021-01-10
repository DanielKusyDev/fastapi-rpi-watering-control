from fastapi import APIRouter, Depends

from api.dependencies.db import PaginationParams
from db import Mongo
from models.domain.plants import Plant
from models.schemas import ListOfPlants, AddPlantInput

router = APIRouter()
db = Mongo("plants")


@router.get(path="", response_model=ListOfPlants)
async def get_plants_list(pagination_params: PaginationParams = Depends(PaginationParams)):
    results = pagination_params.paginate(db.all(apply=False), ListOfPlants)
    return results


@router.post(path="", response_model=Plant)
async def add_plant(plant: AddPlantInput):
    _id = db.insert(**dict(plant))
    raw_plant = db.get_one(_id=_id)
    return Plant(**raw_plant)
