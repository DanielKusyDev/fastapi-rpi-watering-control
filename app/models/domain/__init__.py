import datetime

from bson import ObjectId
from bson.objectid import InvalidId
from pydantic import BaseModel, BaseConfig as PydanticConfig, Field


def convert_datetime_to_realworld(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


def convert_field_to_camel_case(string: str) -> str:
    return "".join(
        word if index == 0 else word.capitalize()
        for index, word in enumerate(string.split("_"))
    )


class BaseConfig(PydanticConfig):
    allow_population_by_field_name = True
    alias_generator = convert_field_to_camel_case


class Model(BaseModel):
    class Config(BaseConfig):
        json_encoders = {datetime.datetime: convert_datetime_to_realworld}


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
            datetime.datetime: convert_datetime_to_realworld
        }

    _id: OID = Field()
