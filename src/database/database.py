import os
from pymongo import MongoClient, collection, database
from dotenv import load_dotenv

load_dotenv()
MongoUri = os.getenv('MONGO_URI')

class Database:    
    def connect_database(database_name:str) -> database.Database:
        try:
            client = MongoClient(MongoUri)
            db = client[database_name]
            return db
        except Exception as e:
            raise Exception(f"could not connect to MongoDB: {e}")


    
    def get_collection(collection_name:str) -> collection:
        try:
            return Database.db[collection_name]
        except Exception as e:
            raise Exception(f"could not connect to collecion '{collection_name}': {e}")
    