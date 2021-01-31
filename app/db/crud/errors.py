from db.crud import Connection
from db.models import Error


def add_error(e: Exception):
    with Connection.session_scope() as db:
        error_record = Error(error=str(e), type=e.__class__.__name__)
        db.add(error_record)
        db.commit()
