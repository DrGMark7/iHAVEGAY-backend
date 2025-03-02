from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import Ram, UpdateRam
from src.services.hardware_service import HardwareService

class RamController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('Rams')

    async def get_all(self):
        """Get all RAMs from database"""
        if not self.collection:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, ram_id: int):
        """Get a RAM by its ID"""
        if not self.collection:
            await self._init_collection()
        ram = await self.collection.find_one({"ram_id": ram_id}, {"_id": 0})
        if not ram:
            raise ValueError(f"RAM with id {ram_id} not found")
        return ram

    async def create(self, ram: Ram):
        """Create a new RAM"""
        if not self.collection:
            await self._init_collection()
        ram_dict = ram.model_dump(exclude_none=True)
        result = await self.collection.insert_one(ram_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert RAM")
        return {"message": "RAM added successfully", "id": str(result.inserted_id)}

    async def update(self, ram_id: int, ram: UpdateRam):
        """Update an existing RAM"""
        if not self.collection:
            await self._init_collection()
        update_data = ram.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"ram_id": ram_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"RAM with id {ram_id} not found")
        return {"message": "RAM updated successfully"}

    async def delete(self, ram_id: int):
        """Delete a RAM"""
        if not self.collection:
            await self._init_collection()
        result = await self.collection.delete_one({"ram_id": ram_id})
        if result.deleted_count == 0:
            raise ValueError(f"RAM with id {ram_id} not found")
        return {"message": "RAM deleted successfully", "ram_id": ram_id}
