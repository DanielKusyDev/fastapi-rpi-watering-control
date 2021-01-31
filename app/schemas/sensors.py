from typing import Optional

from pydantic import AnyUrl

from schemas import Schema, DbSchema


class SensorInput(Schema):
    name: str
    kind: str
    gpio_channel: int


class SensorSchema(DbSchema):
    name: str
    kind: str
    plant_id: Optional[int]
    gpio_channel: Optional[int]
    state: Optional[bool]


class AssigningSchema(Schema):
    sensor: AnyUrl
    plant: AnyUrl
