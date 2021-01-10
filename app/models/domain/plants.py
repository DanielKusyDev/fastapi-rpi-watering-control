from models.domain import MongoModel
from typing import Optional

from models.domain.sensors import Sensor


class Plant(MongoModel):
    name: str
    sensor: Optional[Sensor] = None
