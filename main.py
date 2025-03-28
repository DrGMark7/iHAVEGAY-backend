<<<<<<< HEAD

import asyncio
=======
import os
>>>>>>> b1e5cea768ecc0552368c66fc60f74252bdee22e
from typing import Optional, List
from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD

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

# get cpu by cpu_id
@app.get("/CPUs/{cpu_id}", response_model=CPU)
async def getCPUByID(cpu_id: int):
    collection = Database.get_collection('CPUs')
    cpu = await collection.find_one({"cpu_id": cpu_id})
    if cpu is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return cpu

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

@router.patch("/CPUs/{cpu_id}")
async def update_cpu(cpu_id: int, cpu_update: updateCPU):
    collection = Database.get_collection('CPUs')
    if collection is None:
        raise HTTPException(status_code=404, detail="CPU not found")
    
    update_data = {k: v for k, v in cpu_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"cpu_id": cpu_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "CPU updated successfully", "updated_fields": update_data}

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

# get ram by ram_id
@app.get("/Rams/{ram_id}", response_model=Ram)
async def getRamByID(ram_id: int):
    collection = Database.get_collection('Rams')
    ram = await collection.find_one({"ram_id": ram_id})
    if ram is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ram

@router.post("/Rams")
async def add_Ram(Ram: Ram):
    collection = Database.get_collection('Rams')
    Ram_data = Ram.model_dump(exclude_none = True)
    result = await collection.insert_one(Ram_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Ram data")
    
    return {"message": "Ram added successfully", "id": str(result.inserted_id)}

@router.delete("/Rams/{ram_id}")
async def delete_ram(ram_id: int):
    # delete Ram by Ram_id
    collection = Database.get_collection('Rams')
    result = collection.delete_one({'ram_id': ram_id})
    if result:
        return {"detail": "Item deleted successfully", "ram_id": ram_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/Rams/{ram_id}")
async def update_ram(ram_id: int, ram_update: updateRam):
    collection = Database.get_collection('Rams')
    if collection is None:
        raise HTTPException(status_code=404, detail="Ram not found")
    
    update_data = {k: v for k, v in ram_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"ram_id": ram_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "Ram updated successfully", "updated_fields": update_data}

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

# get mainboard by mainboard_id
@app.get("/Mainboards/{mainboard_id}", response_model=Mainboard)
async def getMainboardByID(mainboard_id: int):
    collection = Database.get_collection('Mainboards')
    mainboard = await collection.find_one({"mainboard_id": mainboard_id})
    if mainboard is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return mainboard

@router.post("/Mainboards")
async def add_Mainboard(Mainboard: Mainboard):
    collection = Database.get_collection('Mainboards')
    Mainboard_data = Mainboard.model_dump(exclude_none = True)
    result = await collection.insert_one(Mainboard_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Mainboard data")
    
    return {"message": "Mainboard added successfully", "id": str(result.inserted_id)}

@router.delete("/Mainboards/{mainboard_id}")
async def delete_mainboard(mainboard_id: int):
    # delete Mainboard by Mainboard_id
    collection = Database.get_collection('Mainboards')
    result = collection.delete_one({'mainboard_id': mainboard_id})
    if result:
        return {"detail": "Item deleted successfully", "mainboard_id": mainboard_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/Mainboards/{mainboard_id}")
async def update_mainboard(mainboard_id: int, mainboard_update: updateMainboard):
    collection = Database.get_collection('Mainboards')
    if collection is None:
        raise HTTPException(status_code=404, detail="Mainboard not found")
    
    update_data = {k: v for k, v in mainboard_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"mainboard_id": mainboard_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "Mainboard updated successfully", "updated_fields": update_data}

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

# get ssd by ssd_id
@app.get("/SSDs/{ssd_id}", response_model=SSD)
async def getSSDByID(ssd_id: int):
    collection = Database.get_collection('SSDs')
    ssd = await collection.find_one({"ssd_id": ssd_id})
    if ssd is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ssd

@router.post("/SSDs")
async def add_ssd(SSD: SSD):
    collection = Database.get_collection('SSDs')
    SSD_data = SSD.model_dump(exclude_none = True)
    result = await collection.insert_one(SSD_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert SSD data")
    
    return {"message": "SSD added successfully", "id": str(result.inserted_id)}

@router.delete("/SSDs/{ssd_id}")
async def delete_ssd(ssd_id: int):
    # delete SSD by SSD_id
    collection = Database.get_collection('SSDs')
    result = collection.delete_one({'ssd_id': ssd_id})
    if result:
        return {"detail": "Item deleted successfully", "ssd_id": ssd_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/SSDs/{ssd_id}")
async def update_ssd(ssd_id: int, ssd_update: updateSSD):
    collection = Database.get_collection('SSDs')
    if collection is None:
        raise HTTPException(status_code=404, detail="SSD not found")
    
    update_data = {k: v for k, v in ssd_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"ssd_id": ssd_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "SSD updated successfully", "updated_fields": update_data}

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

# get m2 by m2_id
@app.get("/M2s/{m2_id}", response_model=M2)
async def getM2ByID(m2_id: int):
    collection = Database.get_collection('M2s')
    m2 = await collection.find_one({"m2_id": m2_id})
    if m2 is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return m2

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

@router.patch("/M2s/{m2_id}")
async def update_m2(m2_id: int, m2_update: updateM2):
    collection = Database.get_collection('M2s')
    if collection is None:
        raise HTTPException(status_code=404, detail="M2 not found")
    
    update_data = {k: v for k, v in m2_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"m2_id": m2_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "M2 updated successfully", "updated_fields": update_data}

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

# get gpu by gpu_id
@app.get("/GPUs/{gpu_id}", response_model=GPU)
async def getGPUByID(gpu_id: int):
    collection = Database.get_collection('GPUs')
    gpu = await collection.find_one({"gpu_id": gpu_id})
    if gpu is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return gpu

@router.post("/GPUs")
async def add_gpu(GPU: GPU):
    collection = Database.get_collection('GPUs')
    GPU_data = GPU.model_dump(exclude_none = True)
    result = await collection.insert_one(GPU_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert GPU data")
    
    return {"message": "GPU added successfully", "id": str(result.inserted_id)}

@router.delete("/GPUs/{gpu_id}")
async def delete_gpu(gpu_id: int):
    # delete GPU by GPU_id
    collection = Database.get_collection('GPUs')
    result = collection.delete_one({'gpu_id': gpu_id})
    if result:
        return {"detail": "Item deleted successfully", "gpu_id": gpu_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/GPUs/{gpu_id}")
async def update_gpu(gpu_id: int, gpu_update: updateGPU):
    collection = Database.get_collection('GPUs')
    if collection is None:
        raise HTTPException(status_code=404, detail="GPU not found")
    
    update_data = {k: v for k, v in gpu_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"gpu_id": gpu_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "GPU updated successfully", "updated_fields": update_data}

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

# get case by case_id
@app.get("/Cases/{case_id}", response_model=Case)
async def getCaseByID(case_id: int):
    collection = Database.get_collection('Cases')
    case = await collection.find_one({"case_id": case_id})
    if case is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return case

@router.post("/Cases")
async def add_case(Case: Case):
    collection = Database.get_collection('Cases')
    Case_data = Case.model_dump(exclude_none = True)
    result = await collection.insert_one(Case_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert Case data")
    
    return {"message": "Case added successfully", "id": str(result.inserted_id)}

@router.delete("/Cases/{case_id}")
async def delete_case(case_id: int):
    # delete Case by Case_id
    collection = Database.get_collection('Cases')
    result = collection.delete_one({'case_id': case_id})
    if result:
        return {"detail": "Item deleted successfully", "case_id": case_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/Cases/{case_id}")
async def update_case(case_id: int, case_update: updateCase):
    collection = Database.get_collection('Cases')
    if collection is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    update_data = {k: v for k, v in case_update.model_dump().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    # Update in MongoDB
    result = await collection.update_one({"case_id": case_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")

    return {"message": "Case updated successfully", "updated_fields": update_data}

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

# get psu by psu_id
@app.get("/PSUs/{psu_id}", response_model=PSU)
async def getPSUByID(psu_id: int):
    collection = Database.get_collection('PSUs')
    psu = await collection.find_one({"psu_id": psu_id})
    if psu is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return psu

@router.post("/PSUs")
async def add_psu(PSU: PSU):
    collection = Database.get_collection('PSUs')
    PSU_data = PSU.model_dump(exclude_none = True)
    result = await collection.insert_one(PSU_data)

    if not result.inserted_id:
        raise HTTPException(status_code=500, detail="Failed to insert PSU data")
    
    return {"message": "PSU added successfully", "id": str(result.inserted_id)}

@router.delete("/PSUs/{psu_id}")
async def delete_psu(psu_id: int):
    # delete PSU by PSU_id
    collection = Database.get_collection('PSUs')
    result = collection.delete_one({'psu_id': psu_id})
    if result:
        return {"detail": "Item deleted successfully", "PSU_id": psu_id}
    raise HTTPException(status_code=404, detail="Item not found")

@router.patch("/PSUs/{psu_id}")
async def update_psu(psu_id: int, psu_update: updatePSU):
    collection = Database.get_collection('PSUs')
    existing_psu = await collection.find_one({"psu_id": psu_id})
    if not existing_psu:
        raise HTTPException(status_code=404, detail="PSU not found")
    print("Existing PSU:", existing_psu)
    
    update_data = {k: v for k, v in psu_update.model_dump().items() if v is not None}
    print("Update Data:", update_data)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    
    changes_detected = False
    for key, value in update_data.items():
        if existing_psu.get(key) != value:
            changes_detected = True
            break
    
    if not changes_detected:
        raise HTTPException(status_code=400, detail="No changes detected in the provided data")
    
    # Update in MongoDB
    result = await collection.update_one({"psu_id": psu_id}, {"$set": update_data})

    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="No changes made")
    
    return {"message": "PSU updated successfully", "updated_fields": update_data}

app.include_router(router)
=======
from src.database.database import Database
from src.models.hardware_models import CPU
from src.routes import (
    cpu_router,
    ram_router,
    mainboard_router,
    storage_router,
    gpu_router,
    case_router,
    psu_router
)

# Initialize FastAPI app
app = FastAPI(
    title="Computer Parts API",
    description="API for managing computer hardware components",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
>>>>>>> b1e5cea768ecc0552368c66fc60f74252bdee22e
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในการใช้งานจริงควรระบุ origins ที่อนุญาตเท่านั้น
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database Connection
@app.on_event("startup")
async def startup_db_client():
    try:
        Database.get_instance()
        print("Database connection initialized")
    except Exception as e:
        print(f"Failed to initialize database connection: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    try:
        Database.close_connection()
        print("Database connection closed")
    except Exception as e:
        print(f"Error closing database connection: {e}")

# Register routes with prefix
api_prefix = "/api/v1"
app.include_router(cpu_router, prefix=api_prefix)
app.include_router(ram_router, prefix=api_prefix)
app.include_router(mainboard_router, prefix=api_prefix)
app.include_router(storage_router, prefix=api_prefix)
app.include_router(gpu_router, prefix=api_prefix)
app.include_router(case_router, prefix=api_prefix)
app.include_router(psu_router, prefix=api_prefix)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint providing API information and documentation links
    """
    return {
        "message": "Welcome to Computer Parts API",
        "version": "1.0.0",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API and database status
    """
    try:
        db_status = "connected" if Database.is_connected() else "disconnected"
        return {
            "status": "healthy",
            "database": db_status,
            "api_version": "1.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    # Load configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "True").lower() == "true"
    workers = int(os.getenv("WORKERS", 1))
    
    # Configure logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers,
        log_config=log_config
    )

