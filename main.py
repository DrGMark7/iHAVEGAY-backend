from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.database.database import Database
from src.database.datamodel import CPU


app = FastAPI()
router = APIRouter()

@router.get("/CPUs", response_model=List[CPU])
async def get_cpu():

    # get CPU from database and return list of CPUs

    collection = Database.get_collection('CPUs')
    datas = await collection.find({}, {"_id": 0})

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No CPU data found"})
    return [data for data in datas]


@router.post("/CPUs")
async def add_cpu(cpu: CPU):
    collection = Database.get_collection('CPUs')
    cpu_data = cpu.model_dump(exclude_none = True)
    result = await collection.insert_one(cpu_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert CPU data")
    
    return {"message": "CPU added successfully", "id": str(result.inserted_id)}


@router.delete("/CPUs/{cpu_id}")
async def delete_item(cpu_id: int):
    # delete cpu by cpu_id
    collection = Database.get_collection('CPUs')
    result = await collection.find_one_and_delete({"id": cpu_id})
    if result:
        return result
    raise HTTPException(status_code=404, detail="Item not found")

app.include_router(router)


