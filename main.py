import asyncio
from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from src.database.database import Database
from src.database.datamodel import CPU, Ram, Mainboard, SSD, M2, GPU, Case, PSU


app = FastAPI()
router = APIRouter()


@router.get("/CPUs", response_model=List[CPU])
async def get_cpu():
    # get CPU from database and return list of CPUs
    collection = Database.get_collection('CPUs')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No CPU data found"})
    return datas


@router.post("/CPUs")
async def add_cpu(cpu: CPU):
    collection = Database.get_collection('CPUs')
    cpu_data = cpu.model_dump(exclude_none = True)
    result = await collection.insert_one(cpu_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert CPU data")
    
    return {"message": "CPU added successfully", "id": str(result.inserted_id)}


@router.delete("/CPUs/{cpu_id}")
async def delete_cpu(cpu_id: int):
    # delete cpu by cpu_id
    collection = Database.get_collection('CPUs')
    result = collection.delete_one({'cpu_id': cpu_id})
    if result:
        return {"detail": "Item deleted successfully", "cpu_id": cpu_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/Rams", response_model=List[Ram])
async def get_Ram():
    # get Ram from database and return list of Rams
    collection = Database.get_collection('Rams')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No Ram data found"})
    return datas


@router.post("/Rams")
async def add_Ram(Ram: Ram):
    collection = Database.get_collection('Rams')
    Ram_data = Ram.model_dump(exclude_none = True)
    result = await collection.insert_one(Ram_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Ram data")
    
    return {"message": "Ram added successfully", "id": str(result.inserted_id)}


@router.delete("/Rams/{Ram_id}")
async def delete_ram(Ram_id: int):
    # delete Ram by Ram_id
    collection = Database.get_collection('Rams')
    result = collection.delete_one({'Ram_id': Ram_id})
    if result:
        return {"detail": "Item deleted successfully", "Ram_id": Ram_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/Mainboards", response_model=List[Mainboard])
async def get_Mainboard():
    # get Mainboard from database and return list of Mainboards
    collection = Database.get_collection('Mainboards')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No Mainboard data found"})
    return datas


@router.post("/Mainboards")
async def add_Mainboard(Mainboard: Mainboard):
    collection = Database.get_collection('Mainboards')
    Mainboard_data = Mainboard.model_dump(exclude_none = True)
    result = await collection.insert_one(Mainboard_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Mainboard data")
    
    return {"message": "Mainboard added successfully", "id": str(result.inserted_id)}


@router.delete("/Mainboards/{Mainboard_id}")
async def delete_mainboard(Mainboard_id: int):
    # delete Mainboard by Mainboard_id
    collection = Database.get_collection('Mainboards')
    result = collection.delete_one({'Mainboard_id': Mainboard_id})
    if result:
        return {"detail": "Item deleted successfully", "Mainboard_id": Mainboard_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/SSDs", response_model=List[SSD])
async def get_ssd():
    # get SSD from database and return list of SSDs
    collection = Database.get_collection('SSDs')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No SSD data found"})
    return datas


@router.post("/SSDs")
async def add_ssd(SSD: SSD):
    collection = Database.get_collection('SSDs')
    SSD_data = SSD.model_dump(exclude_none = True)
    result = await collection.insert_one(SSD_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert SSD data")
    
    return {"message": "SSD added successfully", "id": str(result.inserted_id)}


@router.delete("/SSDs/{SSD_id}")
async def delete_ssd(SSD_id: int):
    # delete SSD by SSD_id
    collection = Database.get_collection('SSDs')
    result = collection.delete_one({'SSD_id': SSD_id})
    if result:
        return {"detail": "Item deleted successfully", "SSD_id": SSD_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.get("/M2s", response_model=List[M2])
async def get_m2():
    # get M2 from database and return list of M2
    collection = Database.get_collection('M2s')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No M2 data found"})
    return datas


@router.post("/M2s")
async def add_m2(M2: M2):
    collection = Database.get_collection('M2s')
    M2_data = M2.model_dump(exclude_none = True)
    result = await collection.insert_one(M2_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert M2 data")
    
    return {"message": "M2 added successfully", "id": str(result.inserted_id)}


@router.delete("/M2s/{M2_id}")
async def delete_m2(M2_id: int):
    # delete M2 by M2_id
    collection = Database.get_collection('M2s')
    result = collection.delete_one({'m2_id': M2_id})
    if result:
        return {"detail": "Item deleted successfully", "M2_id": M2_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/GPUs", response_model=List[GPU])
async def get_gpu():
    # get GPU from database and return list of GPU
    collection = Database.get_collection('GPUs')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No GPU data found"})
    return datas


@router.post("/GPUs")
async def add_gpu(GPU: GPU):
    collection = Database.get_collection('GPUs')
    GPU_data = GPU.model_dump(exclude_none = True)
    result = await collection.insert_one(GPU_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert GPU data")
    
    return {"message": "GPU added successfully", "id": str(result.inserted_id)}


@router.delete("/GPUs/{GPU_id}")
async def delete_gpu(GPU_id: int):
    # delete GPU by GPU_id
    collection = Database.get_collection('GPUs')
    result = collection.delete_one({'GPU_id': GPU_id})
    if result:
        return {"detail": "Item deleted successfully", "GPU_id": GPU_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/Cases", response_model=List[Case])
async def get_case():
    # get Case from database and return list of Case
    collection = Database.get_collection('Cases')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No Case data found"})
    return datas


@router.post("/Cases")
async def add_case(Case: Case):
    collection = Database.get_collection('Cases')
    Case_data = Case.model_dump(exclude_none = True)
    result = await collection.insert_one(Case_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Case data")
    
    return {"message": "Case added successfully", "id": str(result.inserted_id)}


@router.delete("/Cases/{Case_id}")
async def delete_case(Case_id: int):
    # delete Case by Case_id
    collection = Database.get_collection('Cases')
    result = collection.delete_one({'Case_id': Case_id})
    if result:
        return {"detail": "Item deleted successfully", "Case_id": Case_id}
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/PSUs", response_model=List[PSU])
async def get_psu():
    # get PSU from database and return list of PSU
    collection = Database.get_collection('PSUs')
    cursor = collection.find({}, {"_id": 0})
    datas = []
    
    async for document in cursor:
        datas.append(document)

    if not datas:
        return JSONResponse(status_code=404, content={"message": "No PSU data found"})
    return datas


@router.post("/PSUs")
async def add_psu(PSU: PSU):
    collection = Database.get_collection('PSUs')
    PSU_data = PSU.model_dump(exclude_none = True)
    result = await collection.insert_one(PSU_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert PSU data")
    
    return {"message": "PSU added successfully", "id": str(result.inserted_id)}


@router.delete("/PSUs/{PSU_id}")
async def delete_psu(PSU_id: int):
    # delete PSU by PSU_id
    collection = Database.get_collection('PSUs')
    result = collection.delete_one({'PSU_id': PSU_id})
    if result:
        return {"detail": "Item deleted successfully", "PSU_id": PSU_id}
    raise HTTPException(status_code=404, detail="Item not found")

app.include_router(router)


