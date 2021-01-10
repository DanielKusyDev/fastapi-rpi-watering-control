from typing import Optional, ClassVar

from fastapi import Query
from pymongo.cursor import Cursor

from core.config import DEFAULT_PAGINATION_SIZE
from models.schemas import PaginatedResponse


class PaginationParams:
    def __init__(self, page: int = Query(default=1, gt=0),  page_size: Optional[int] = DEFAULT_PAGINATION_SIZE):
        self.page = page
        self.page_size = page_size

    def paginate(self, db: Cursor, response_class: ClassVar[PaginatedResponse]) -> list:
        skip_by = (self.page - 1) * self.page_size
        cursor = db.limit(self.page_size).skip(skip_by)
        results = list(cursor)
        instance = response_class(results=results, count=len(results), page=self.page)
        return instance
