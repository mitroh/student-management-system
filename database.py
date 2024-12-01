from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

from pymongo import MongoClient


mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database()
def to_response_id(obj):
  
    if "_id" in obj:
        obj["id"] = str(obj.pop("_id"))
    return obj