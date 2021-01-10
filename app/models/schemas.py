from typing import List

from models.domain import Model
from models.domain.plants import Plant


class CreatePlantInput(Model):
    name: str


class ListOfPlants(Model):
    plants: List[Plant]
