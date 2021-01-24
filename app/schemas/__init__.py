import datetime
from typing import List, Any

from pydantic import BaseModel, BaseConfig


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class Schema(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}
        allow_population_by_field_name = True
        alias_generator = convert_field_to_camel_case


class DbSchema(Schema):
    id: int
    add_date: datetime.datetime

    class Config:
        orm_mode = True


class PaginatedResponse(Schema):
    page: int
    count: int
    results: List[Any] = []

    def to_schema(self, schema_cls):
        schema_results = []
        for obj in self.results:
            schema_results.append(schema_cls(**obj.__dict__))
        return self


class IdAndUrlSchema(Schema):
    id: int
    url: str = ""
