from fastapi import APIRouter, Depends

from api.dependencies import PaginationParams
from db import crud
from schemas import PaginatedResponse
from schemas.sensors import CreateResponse, SensorSchema, DbSensorSchema

router = APIRouter()


@router.get(path="", response_model=PaginatedResponse)
async def get_sensors_list(pagination_params: PaginationParams = Depends(PaginationParams)):
    plants = crud.get_sensors_list(pagination_params)
    response = PaginatedResponse(page=pagination_params.page, count=len(plants), results=plants)
    return response


@router.post(path="", response_model=CreateResponse, status_code=201)
async def add_sensor(sensor: SensorSchema):
    db_sensor = crud.create_sensor(sensor)
    return CreateResponse(id=db_sensor.id)


@router.put(path="/{sensor_id}/{plant_id}", response_model=SensorSchema)
async def assign_sensor_to_plant(sensor_id: int, plant_id: int):
    sensor = crud.assign_sensor_to_plant(sensor_id, plant_id)
    return DbSensorSchema(**sensor.__dict__)
