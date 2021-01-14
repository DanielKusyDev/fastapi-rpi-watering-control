from fastapi import APIRouter, Depends
from starlette.requests import Request

from api.dependencies import PaginationParams
from db import crud
from schemas import PaginatedResponse
from schemas.sensors import CreateResponse, SensorInput, SensorSchema, AssigningSchema

router = APIRouter()


@router.get(path="", response_model=PaginatedResponse)
async def get_sensors_list(pagination_params: PaginationParams = Depends(PaginationParams)):
    sensors = crud.get_sensors_list(pagination_params)
    response = PaginatedResponse(page=pagination_params.page, count=len(sensors), results=sensors)
    return response


@router.post(path="", response_model=CreateResponse, status_code=201)
async def add_sensor(request: Request, sensor: SensorInput):
    db_sensor = crud.create_sensor(sensor)
    return {
        "id": db_sensor.id,
        "url": request.url_for("get_sensor_details", sensor_id=db_sensor.id)
    }


@router.get(path="/{sensor_id}", response_model=SensorSchema)
async def get_sensor_details(sensor_id: int):
    sensor = crud.get_sensor(sensor_id)
    return sensor


@router.put(path="/{sensor_id}/{plant_id}", response_model=AssigningSchema)
async def assign_sensor_to_plant(request: Request, sensor_id: int, plant_id: int):
    plant = crud.assign_sensor_to_plant(sensor_id, plant_id)
    return {
        "sensor": request.url_for("get_sensor_details", sensor_id=sensor_id),
        "plant": request.url_for("get_plant_details", plant_id=plant_id)
    }
