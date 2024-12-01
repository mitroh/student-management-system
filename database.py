from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://rohanmittalsnp:18RE7aTAh7pS7JOc@cluster0.epomb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = AsyncIOMotorClient(MONGO_URI)
db = client.student_management

# def to_response_id(obj):
#     obj["id"] = str(obj.pop("_id"))
#     return obj
def to_response_id(obj):
    # """Convert MongoDB `_id` to `id`."""
    if "_id" in obj:
        obj["id"] = str(obj.pop("_id"))
    return obj