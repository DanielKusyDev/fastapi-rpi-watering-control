from typing import List

from schemas import Schema, DbSchema
from schemas.sensors import SensorSchema


class PlantInput(Schema):
    name: str


class PlantSchema(DbSchema):
    sensors: List[SensorSchema]
    water_level: bool = False
