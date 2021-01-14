from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.dependencies import PaginationParams
from db import crud
from schemas.sensors import PaginatedResponse, CreateResponse, PlantInput, PlantSchema

router = APIRouter()


@router.get(path="", response_model=PaginatedResponse)
async def get_plants_list_req(pagination_params: PaginationParams = Depends(PaginationParams)):
    plants = crud.get_plants_list(pagination_params)
    response = PaginatedResponse(page=pagination_params.page, count=len(plants), results=plants).to_schema(PlantSchema)
    return response


@router.post(path="", response_model=CreateResponse, status_code=201)
async def add_plant(request: Request, plant: PlantInput):
    db_plant = crud.create_plant(plant)
    return {
        "id": db_plant.id,
        "url": request.url_for("get_sensor_details", sensor_id=db_plant.id)
    }


@router.get(path="/{plant_id}", response_model=PlantSchema)
async def get_plant_details(sensor_id: int):
    plant = crud.get_plant(sensor_id)
    return plant
