from typing import Optional

from fastapi import Query

from db.models import Plant
from schemas import Schema, DbSchema


class CreateResponse(Schema):
    id: int
    url: str = ""


class PaginatedResponse(Schema):
    page: int
    count: int
    results: list = []


class SensorSchema(Schema):
    name: str


class DbSensorSchema(DbSchema):
    name: str
    plant_id: Optional[int]


class PlantSchema(Schema):
    name: str


class GpioSchema(Schema):
    pin: int
    state: bool


class DbGpioSchema(DbSchema):
    pin: int
    state: bool
