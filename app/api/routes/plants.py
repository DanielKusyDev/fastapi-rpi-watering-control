from fastapi import APIRouter, Depends

from api.dependencies import PaginationParams
from db import crud
from schemas.sensors import PaginatedResponse, CreateResponse, PlantSchema

router = APIRouter()


@router.get(path="", response_model=PaginatedResponse)
async def get_plants_list_req(pagination_params: PaginationParams = Depends(PaginationParams)):
    plants = crud.get_plants_list(pagination_params)
    response = PaginatedResponse(page=pagination_params.page, count=len(plants), results=plants)
    return response


@router.post(path="", response_model=CreateResponse, status_code=201)
async def add_plant(plant: PlantSchema):
    db_plant = crud.create_plant(plant)
    return CreateResponse(id=db_plant.id)
