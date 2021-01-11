from contextlib import contextmanager
from functools import wraps

from sqlalchemy.orm import Session, Query

from api.dependencies import PaginationParams
from app.db import models, SessionLocal
from db.models import Plant, Base
from schemas.sensors import PlantSchema


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


def get_plants_list(pagination_params: PaginationParams = None):
    with session_scope() as db:
        q = db.query(models.Plant)
        plants = paginate(q, pagination_params)
    return plants


def create_plant(data: PlantSchema):
    with session_scope() as db:
        plant = Plant(name=data.name)
        plant = add_and_refresh(db, plant)
    return plant
