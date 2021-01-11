from contextlib import contextmanager
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from api.dependencies import PaginationParams
from app.db import models, SessionLocal
from db.models import Plant, Base, Sensor, GpioInput
from schemas.sensors import PlantSchema, SensorSchema


def paginate(db: Query, pagination_params: PaginationParams):
    if pagination_params is not None:
        offset = (pagination_params.page - 1) * pagination_params.page_size
        return db.offset(offset).limit(pagination_params.page_size).all()
    return db


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def add_and_refresh(db: Session, instance: Base):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def all(cls: Base, pagination_params: PaginationParams = None) -> List[Base]:
    with session_scope() as db:
        q = db.query(cls)
        plants = paginate(q, pagination_params)
    return plants


def get_plants_list(pagination_params: PaginationParams = None) -> List[Plant]:
    return all(models.Plant, pagination_params)


def create_plant(data: PlantSchema) -> Plant:
    with session_scope() as db:
        plant = Plant(name=data.name)
        plant = add_and_refresh(db, plant)
    return plant


def get_sensors_list(pagination_params: PaginationParams = None) -> List[models.Sensor]:
    return all(models.Sensor, pagination_params)


def create_sensor(data: SensorSchema) -> Sensor:
    with session_scope() as db:
        sensor = Sensor(name=data.name)
        sensor = add_and_refresh(db, sensor)
    return sensor


def get_gpio_inputs() -> List[GpioInput]:
    return all(GpioInput)


def assign_sensor_to_plant(sensor_id: int, plant_id: int):
    with session_scope() as db:
        sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
        plant = db.query(Plant).filter(Plant.id == plant_id).first()
        if sensor and plant:
            sensor.plant_id = plant_id
            db.commit()
            db.refresh(sensor)
        else:
            raise HTTPException(status_code=404)
    return sensor
