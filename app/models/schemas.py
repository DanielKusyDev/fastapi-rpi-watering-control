from typing import List

from models.domain import Model
from models.domain.plants import Plant


class PaginatedResponse(Model):
    count: int
    next: str
    results: list


class CreatePlantInput(Model):
    name: str


class ListOfPlants(PaginatedResponse):
    results: List[Plant]
