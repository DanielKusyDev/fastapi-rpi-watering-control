from typing import Optional

from pydantic import AnyUrl

from schemas import Schema, DbSchema


class SensorInput(Schema):
    name: str


class SensorSchema(DbSchema):
    name: str
    plant_id: Optional[int]


class AssigningSchema(Schema):
    sensor: AnyUrl
    plant: AnyUrl
