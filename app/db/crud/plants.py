from typing import List

from api.dependencies import PaginationParams
from db import models
from db.crud import Connection
from schemas.plants import PlantInput


def get_plants_list(pagination_params: PaginationParams = None) -> List[models.Plant]:
    with Connection.session_scope() as db:
        q = db.query(models.Plant).outerjoin(models.Sensor)
        q = Connection.paginate(q, pagination_params)
    return q.all()


def create_plant(data: PlantInput) -> models.Plant:
    with Connection.session_scope() as db:
        plant = models.Plant(name=data.name)
        plant = Connection.add_and_refresh(db, plant)
    return plant


def get_plant(plant_id: int) -> models.Plant:
    with Connection.session_scope() as db:
        plant = db.query(models.Plant).join().filter_by(id=plant_id).one()
        return plant
