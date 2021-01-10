from bson import SON, ObjectId
from fastapi import HTTPException
from pymongo import MongoClient

from core.config import MONGODB_CONFIG

client = MongoClient(host=MONGODB_CONFIG["url"], port=MONGODB_CONFIG["port"])


class Mongo:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.db = getattr(client, MONGODB_CONFIG["db"])
        self.collection = getattr(self.db, collection_name)

    def all(self):
        return self.filter()

    def filter(self, **kwargs):
        cursor = self.collection.find(kwargs)
        return cursor

    def get_one(self, raise_404=True, **kwargs):
        if "_id" in kwargs and not isinstance(kwargs["_id"], ObjectId):
            kwargs["_id"] = ObjectId(kwargs["_id"])
        result = self.collection.find_one(kwargs)
        if not result and raise_404:
            raise HTTPException(status_code=404)
        return result

    def insert(self, many=False, **data):
        insertion_fn = self.collection.insert_many if many else self.collection.insert_one
        _id = insertion_fn(data).inserted_id
        return str(_id)

    def update(self, data: dict, many=False, **filters):
        update_fn = self.collection.update_many if many else self.collection.update_one
        update_fn(filters, {"$set": data})
        return data

    def delete(self, many=False, **kwargs):
        delete_fn = self.collection.delete_many if many else self.collection.delete_one
        delete_fn(kwargs)
        return kwargs

    def aggregate(self, pipeline, evaluate=True):
        result = self.collection.aggregate(pipeline)
        return list(result) if evaluate else result

    def count(self):
        return self.collection.count()


class AggregationPipeline:
    def __init__(self):
        self.pipeline = []

    def add_projection(self, **kwargs):
        projection = {"$project": {}}
        for key, value in kwargs.items():
            projection["$project"][key] = value
        self.pipeline.append(projection)

    def add_match(self, **kwargs):
        match = {"$match": {}}
        for key, value in kwargs.items():
            match["$match"][key] = value
        self.pipeline.append(match)

    def add_group(self, **kwargs):
        grouping = {"$group": {}}
        for key, value in kwargs.items():
            grouping["$group"][key] = value
        self.pipeline.append(grouping)

    def add_sorting(self, order_by: list):
        ordering = [(field, 1) for field in order_by]
        sorting = {"$sort": SON(ordering)}
        return sorting