from fastapi import APIRouter, Depends

from api.dependencies.db import PaginationParams
from db import Mongo
from models.domain.plants import Sensor
from models.schemas import AddSensorInput, ListOfSensors

router = APIRouter()
db = Mongo("sensors")


@router.post(path="")
async def add_sensor(sensor: AddSensorInput):
    sensor_as_dict = dict(sensor)
    _id = db.insert(**sensor_as_dict)
    raw_sensor = db.get_one(_id=_id)
    return Sensor(**raw_sensor)


@router.get(path="", response_model=ListOfSensors)
async def get_plants_list(pagination_params: PaginationParams = Depends(PaginationParams)):
    results = pagination_params.paginate(db.all(apply=False), ListOfSensors)
    return results
