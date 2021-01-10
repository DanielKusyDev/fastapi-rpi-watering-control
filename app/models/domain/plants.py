from models.domain import MongoModel
from typing import Optional


class Sensor(MongoModel):
    name: str


class Plant(MongoModel):
    name: str
    sensor: Optional[Sensor] = None
