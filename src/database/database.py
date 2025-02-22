import os
from pymongo import collection
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()
MongoUri = os.getenv('MONGO_URI')

class Database:     
    try:
        client = AsyncIOMotorClient(MongoUri)
        db = client['mydatabase']
    except Exception as e:
        raise Exception(f"could not connect to MongoDB: {e}")


    
    def get_collection(collection_name:str) -> collection.Collection:
        try:
            return Database.db[collection_name]
        except Exception as e:
            raise Exception(f"could not connect to collecion '{collection_name}': {e}")
    