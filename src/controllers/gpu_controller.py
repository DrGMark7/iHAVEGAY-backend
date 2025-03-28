from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import GPU, UpdateGPU
from src.services.hardware_service import HardwareService

class GPUController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('GPUs')

    async def get_all(self):
        """Get all GPUs from database"""
        if self.collection is None:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, gpu_id: int):
        """Get a GPU by its ID"""
        if self.collection is None:
            await self._init_collection()
        gpu = await self.collection.find_one({"gpu_id": gpu_id}, {"_id": 0})
        if not gpu:
            raise ValueError(f"GPU with id {gpu_id} not found")
        return gpu

    async def create(self, gpu: GPU):
        """Create a new GPU"""
        if self.collection is None:
            await self._init_collection()
        gpu_dict = gpu.model_dump(exclude_none=True)
        result = await self.collection.insert_one(gpu_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert GPU")
        return {"message": "GPU added successfully", "id": str(result.inserted_id)}

    async def update(self, gpu_id: int, gpu: UpdateGPU):
        """Update an existing GPU"""
        if self.collection is None:
            await self._init_collection()
        update_data = gpu.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"gpu_id": gpu_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"GPU with id {gpu_id} not found")
        return {"message": "GPU updated successfully"}

    async def delete(self, gpu_id: int):
        """Delete a GPU"""
        if self.collection is None:
            await self._init_collection()
        result = await self.collection.delete_one({"gpu_id": gpu_id})
        if result.deleted_count == 0:
            raise ValueError(f"GPU with id {gpu_id} not found")
        return {"message": "GPU deleted successfully", "gpu_id": gpu_id}
