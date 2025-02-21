# from typing import Union
from fastapi import FastAPI
from src.database.database import Database


app = FastAPI()



@app.get("/CPU/")
async def list_CPU():
    CPU_collection = Database.db['CPU']
    return CPU_collection(CPU=await CPU_collection.find())


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}