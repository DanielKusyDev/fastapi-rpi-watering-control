from fastapi import APIRouter, Depends

from api.dependencies import PaginationParams
from db.crud import get_plants_list
from schemas.sensors import  PaginatedResponse

router = APIRouter()


@router.get(path="", response_model=PaginatedResponse)
async def get_plants_list_req(pagination_params: PaginationParams = Depends(PaginationParams)):
    plants = get_plants_list(pagination_params)
    response = PaginatedResponse(page=pagination_params.page, count=len(plants), results=plants)
    return []

#
# @router.post(path="", response_model=Plant)
# async def add_plant(plant: AddPlantInput):
#     _id = db.insert(**dict(plant))
#     raw_plant = db.get_one(_id=_id)
#     return Plant(**raw_plant)
