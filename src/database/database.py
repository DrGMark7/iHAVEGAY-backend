import os
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from dotenv import load_dotenv
import atexit

# Load environment variables
load_dotenv()

class Database:
    _instance = None
    _client: Optional[AsyncIOMotorClient] = None
    _db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if Database._instance is not None:
            raise Exception("This class is a singleton. Use get_instance() instead")
        else:
            Database._instance = self
            self._connect()
            atexit.register(self.close_connection)

    def _connect(self):
        """
        Connect to MongoDB using environment variables
        """
        try:
            mongo_uri = os.getenv('MONGO_URI')
            if not mongo_uri:
                raise ValueError("MONGO_URI environment variable is not set")

            self._client = AsyncIOMotorClient(mongo_uri)
            self._db = self._client['mydatabase']

            print("Successfully connected to MongoDB")

        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def get_collection(cls, collection_name: str) -> AsyncIOMotorCollection:
        """
        Get a MongoDB collection by name
        """
        instance = cls.get_instance()
        if instance._db is None:
            raise Exception("Database not connected")
        try:
            return instance._db[collection_name]
        except Exception as e:
            raise Exception(f"Failed to get collection '{collection_name}': {e}")

    @classmethod
    def close_connection(cls):
        """
        Close the MongoDB connection
        """
        instance = cls.get_instance()
        if instance._client is not None:
            instance._client.close()
            instance._client = None
            instance._db = None
            print("MongoDB connection closed")

    @classmethod
    async def is_connected(cls) -> bool:
        """
        Check if the database is connected
        """
        instance = cls.get_instance()
        if instance._client is None:
            return False
        try:
            await instance._client.admin.command('ping')
            return True
        except:
            return False

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """
        Get the MongoDB database instance
        """
        instance = cls.get_instance()
        if instance._db is None:
            raise Exception("Database not connected")
        return instance._db

if __name__ == "__main__":
    import asyncio
    
    async def main():
        db_instance = Database.get_instance()
        if await db_instance.is_connected():
            db = db_instance.get_database()
            collections = await db.list_collection_names()
            print("Collections in the database:", collections)
        else:
            print("Database is not connected")
    
    asyncio.run(main())