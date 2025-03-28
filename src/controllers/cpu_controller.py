from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import CPU, UpdateCPU
from src.services.hardware_service import HardwareService

class CPUController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('CPUs')

    async def get_all(self):
        """Get all CPUs from database"""
        if self.collection is None:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, cpu_id: int):
        """Get a CPU by its ID"""
        if self.collection is None:
            await self._init_collection()
        cpu = await self.collection.find_one({"productID": cpu_id}, {"_id": 0})
        if not cpu:
            raise ValueError(f"CPU with id {cpu_id} not found")
        return cpu

    async def create(self, cpu: CPU):
        """Create a new CPU"""
        if self.collection is None:
            await self._init_collection()
        cpu_dict = cpu.model_dump(exclude_none=True)
        result = await self.collection.insert_one(cpu_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert CPU")
        return {"message": "CPU added successfully", "id": str(result.inserted_id)}

    async def update(self, cpu_id: int, cpu: UpdateCPU):
        """Update an existing CPU"""
        if self.collection is None:
            await self._init_collection()
        update_data = cpu.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"productID": cpu_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"CPU with id {cpu_id} not found")
        return {"message": "CPU updated successfully"}

    async def delete(self, cpu_id: int):
        """Delete a CPU"""
        if self.collection is None:
            await self._init_collection()
        result = await self.collection.delete_one({"productID": cpu_id})
        if result.deleted_count == 0:
            raise ValueError(f"CPU with id {cpu_id} not found")
        return {"message": "CPU deleted successfully", "productID": cpu_id} 