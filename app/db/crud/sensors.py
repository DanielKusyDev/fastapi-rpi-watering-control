from typing import List

from api.dependencies import PaginationParams
from db import models
from db.crud import Connection
from schemas.sensors import SensorInput


def get_sensors_list(pagination_params: PaginationParams = None) -> List[models.Sensor]:
    with Connection.session_scope() as db:
        q = db.query(models.Sensor).join()
        q = Connection.paginate(q, pagination_params)
    return q.all()


def get_sensor(sensor_id: int) -> models.Sensor:
    with Connection.session_scope() as db:
        sensor = db.query(models.Sensor).filter_by(id=sensor_id).one()
    return sensor


def create_sensor(data: SensorInput) -> models.Sensor:
    with Connection.session_scope() as db:
        sensor = models.Sensor(name=data.name, kind=data.kind)
        sensor = Connection.add_and_refresh(db, sensor)
    return sensor


def assign_sensor_to_plant(sensor_id: int, plant_id: int):
    with Connection.session_scope() as db:
        sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).one()
        db.query(models.Plant).filter(models.Plant.id == plant_id).one()
        sensor.plant_id = plant_id
        db.commit()
        db.refresh(sensor)
    return sensor



