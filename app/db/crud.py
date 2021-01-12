from contextlib import contextmanager
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.exc import NoResultFound

from api.dependencies import PaginationParams
from app.db import models, SessionLocal
from schemas.sensors import PlantInput, SensorInput


class DbHelper:

    @classmethod
    @contextmanager
    def session_scope(cls) -> Session:
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

    @classmethod
    def paginate(cls, db: Query, pagination_params: PaginationParams):
        if pagination_params is not None:
            offset = (pagination_params.page - 1) * pagination_params.page_size
            return db.offset(offset).limit(pagination_params.page_size)
        return db

    @classmethod
    def add_and_refresh(cls, db: Session, instance: models.Base):
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def all(cls, *args, pagination_params: PaginationParams = None) -> Query:
        with cls.session_scope() as db:
            q = db.query(*args)
            db = cls.paginate(q, pagination_params)
        return db


def get_plants_list(pagination_params: PaginationParams = None) -> List[models.Plant]:
    with DbHelper.session_scope() as db:
        q = db.query(models.Plant).join()
        q = DbHelper.paginate(q, pagination_params)
    return q.all()


def create_plant(data: PlantInput) -> models.Plant:
    with DbHelper.session_scope() as db:
        plant = models.Plant(name=data.name)
        plant = DbHelper.add_and_refresh(db, plant)
    return plant


def get_sensors_list(pagination_params: PaginationParams = None) -> List[models.Sensor]:
    with DbHelper.session_scope() as db:
        q = db.query(models.Sensor).join()
        q = DbHelper.paginate(q, pagination_params)
    return q.all()


def get_sensor(sensor_id: int) -> models.Sensor:
    with DbHelper.session_scope() as db:
        try:
            sensor = db.query(models.Sensor).filter_by(id=sensor_id).one()
        except NoResultFound:
            raise HTTPException(404)
    return sensor


def get_plant(plant_id: int) -> models.Plant:
    with DbHelper.session_scope() as db:
        try:
            sensor = db.query(models.Plant).join().filter_by(id=plant_id).one()
        except NoResultFound:
            raise HTTPException(404)
        return sensor


def create_sensor(data: SensorInput) -> models.Sensor:
    with DbHelper.session_scope() as db:
        sensor = models.Sensor(name=data.name)
        sensor = DbHelper.add_and_refresh(db, sensor)
    return sensor


def get_gpio_inputs() -> List[models.GpioInput]:
    db = DbHelper.all(models.GpioInput)
    result = db.all()
    return result


def assign_sensor_to_plant(sensor_id: int, plant_id: int):
    with DbHelper.session_scope() as db:
        try:
            sensor = db.query(models.Sensor).filter(models.Sensor.id == sensor_id).one()
            db.query(models.Plant).filter(models.Plant.id == plant_id).one()
            sensor.plant_id = plant_id
            db.commit()
            db.refresh(sensor)

        except NoResultFound:
            raise HTTPException(status_code=404)
    return sensor
