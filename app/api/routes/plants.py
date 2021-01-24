from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from starlette.requests import Request

from api.dependencies import PaginationParams
from db.crud import plants as crud
from schemas import PaginatedResponse, IdAndUrlSchema
from schemas.plants import PlantInput, PlantSchema

router = APIRouter()


@router.get(path="", response_model=List[PlantSchema])
async def get_plants_list_req(pagination_params: PaginationParams = Depends(PaginationParams)):
    plants = crud.get_plants_list(pagination_params)
    # response = PaginatedResponse(page=pagination_params.page, count=len(plants), results=plants).to_schema(PlantSchema)
    return plants


@router.post(path="", response_model=IdAndUrlSchema, status_code=201)
async def add_plant(request: Request, plant: PlantInput):
    db_plant = crud.create_plant(plant)
    return {
        "id": db_plant.id,
        "url": request.url_for("get_sensor_details", sensor_id=db_plant.id)
    }


@router.get(path="/{plant_id}", response_model=PlantSchema)
async def get_plant_details(plant_id: int):
    try:
        plant = crud.get_plant(plant_id)
    except NoResultFound:
        raise HTTPException(404)
    return plant
