from contextlib import contextmanager
from functools import wraps

from sqlalchemy.orm import Session, Query

from api.dependencies import PaginationParams
from app.db import models, SessionLocal


def paginate(db: Query, pagination_params: PaginationParams):
    if pagination_params is not None:
        offset = (pagination_params.page - 1) * pagination_params.page_size
        return db.offset(offset).limit(pagination_params.page_size).all()
    return db


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_plants_list(pagination_params: PaginationParams = None):
    with session_scope() as db:
        q = db.query(models.Plant)
        q = paginate(q, pagination_params)
    return q.all()
