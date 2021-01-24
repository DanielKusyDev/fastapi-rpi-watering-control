from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic.networks import AnyUrl
from sqlalchemy.orm.exc import NoResultFound
from starlette.requests import Request

from api.dependencies import PaginationParams
from db import models
from db.crud import sensors as crud
from schemas import IdAndUrlSchema
from schemas.sensors import SensorInput, SensorSchema

router = APIRouter()


@router.get(path="/types", response_model=List[str])
async def get_sensor_types():
    return [e.value for e in models.SensorType]


@router.get(path="", response_model=List[SensorSchema])
async def get_all_sensors(pagination_params: PaginationParams = Depends(PaginationParams)):
    sensors = crud.get_sensors_list(pagination_params)
    return sensors


@router.post(path="", response_model=IdAndUrlSchema, status_code=201)
async def add_new_sensor(request: Request, sensor: SensorInput):
    db_sensor = crud.create_sensor(sensor)
    return {
        "id": db_sensor.id,
        "url": request.url_for("get_sensor_details", sensor_id=db_sensor.id)
    }


@router.get(path="/{sensor_id}", response_model=SensorSchema)
async def get_sensor_details(sensor_id: int):
    try:
        sensor = crud.get_sensor(sensor_id)
    except NoResultFound:
        raise HTTPException(status_code=404)
    return sensor


@router.put(path="/{sensor_id}/{plant_id}", response_model=Dict[str, AnyUrl])
async def assign_sensor_to_plant(request: Request, sensor_id: int, plant_id: int):
    try:
        crud.assign_sensor_to_plant(sensor_id, plant_id)
    except NoResultFound:
        raise HTTPException(status_code=404)
    return {
        "sensor": request.url_for("get_sensor_details", sensor_id=sensor_id),
        "plant": request.url_for("get_plant_details", plant_id=plant_id)
    }
