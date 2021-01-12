from typing import Optional, List, Any

from db.models import Plant
from schemas import Schema, DbSchema
from pydantic import AnyUrl


class CreateResponse(Schema):
    id: int
    url: str = ""


class PaginatedResponse(Schema):
    page: int
    count: int
    results: List[Any] = []

    def to_schema(self, schema_cls):
        schema_results = []
        for obj in self.results:
            schema_results.append(schema_cls(**obj.__dict__))
        return self


class SensorInput(Schema):
    name: str


class SensorSchema(DbSchema):
    name: str
    plant_id: Optional[int]


class PlantInput(Schema):
    name: str


class PlantSchemaWithoutSensor(DbSchema):
    name: str


class PlantSchema(PlantSchemaWithoutSensor):
    sensor: Optional[SensorSchema]


class GpioInput(Schema):
    pin: int
    state: bool


class GpioSchema(DbSchema):
    pin: int
    state: bool


class AssigningSchema(Schema):
    sensor: AnyUrl
    plant: AnyUrl
