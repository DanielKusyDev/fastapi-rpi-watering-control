from contextlib import contextmanager

from fastapi import HTTPException

from db.crud.errors import add_error


@contextmanager
def error_sentinel(status_code=400, detail=None, exc_type=Exception):
    try:
        yield
    except exc_type as e:
        add_error(e)
        raise HTTPException(status_code=status_code, detail=detail)
