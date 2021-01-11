from typing import Optional

from schemas import Schema, DbSchemaMixin


class CreateResponse(Schema):
    id: int
    url: str = ""


class PaginatedResponse(Schema):
    page: int
    count: int
    results: list = []


class SensorSchema(Schema):
    name: str
    plant_id: Optional[int] = None


class PlantSchema(Schema):
    name: str


class GpioSchema(Schema):
    pin: int
    state: bool


class DbGpioSchema(DbSchemaMixin, GpioSchema):
    pass


class DbSensorSchema(DbSchemaMixin, SensorSchema):
    plant: Optional["DbPlantSchema"] = None


class DbPlantSchema(DbSchemaMixin, PlantSchema):
    sensor: Optional["DbSensorSchema"] = None
