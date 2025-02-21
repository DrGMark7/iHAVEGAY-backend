import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = os.getenv('MONGO_URI')

class Database:
    def __init__(self) -> None:
        self.db = client['mydatabase']
        
