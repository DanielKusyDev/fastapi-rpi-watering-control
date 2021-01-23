import logging
from contextlib import contextmanager
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.exc import NoResultFound

from api.dependencies import PaginationParams
from db import models, SessionLocal
from schemas.sensors import PlantInput, SensorInput


class Connection:

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
