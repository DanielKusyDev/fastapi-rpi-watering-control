from fastapi import APIRouter

from models.domain.plants import Plant
from models.schemas import ListOfPlants, CreatePlantInput

router = APIRouter()


@router.get(path="", response_model=ListOfPlants)
async def get_plants_list():
    ps = [Plant(name="Danielcio", _id="5ffae88791e1b8e2b3fc3919") for i in range(10)]
    return ListOfPlants(plants=ps)


@router.post(path="", response_model=CreatePlantInput)
async def add_plant():
    pass
