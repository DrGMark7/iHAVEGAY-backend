from pymongo import MongoClient

class DatabaseClient:
    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client['mydatabase']
        self.collection = self.db['mycollection']

    def insert(self, data):
        self.collection.insert_one(data)

    def find(self, query):
        return self.collection.find(query)

    def update(self, query, data):
        self.collection.update_one(query, data)

    def delete(self, query):
        self.collection.delete_one(query)