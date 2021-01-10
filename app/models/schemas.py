from typing import List

from pydantic import Field

from models.domain import Model
from models.domain.gpio import GpioField
from models.domain.plants import Plant, Sensor


class PaginatedResponse(Model):
    page: int
    count: int
    results: list


class AddPlantInput(Model):
    name: str


class ListOfPlants(PaginatedResponse):
    results: List[Plant]


class AddSensorInput(Model):
    name: str
    gpio: GpioField = Field()


class ListOfSensors(PaginatedResponse):
    results: List[Sensor]
