from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import PSU, UpdatePSU
from src.services.hardware_service import HardwareService

class PSUController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('PSUs')

    async def get_all(self):
        """Get all PSUs from database"""
        if self.collection is None:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, psu_id: int):
        """Get a PSU by its ID"""
        if self.collection is None:
            await self._init_collection()
        psu = await self.collection.find_one({"psu_id": psu_id}, {"_id": 0})
        if not psu:
            raise ValueError(f"PSU with id {psu_id} not found")
        return psu

    async def create(self, psu: PSU):
        """Create a new PSU"""
        if self.collection is None:
            await self._init_collection()
        psu_dict = psu.model_dump(exclude_none=True)
        result = await self.collection.insert_one(psu_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert PSU")
        return {"message": "PSU added successfully", "id": str(result.inserted_id)}

    async def update(self, psu_id: int, psu: UpdatePSU):
        """Update an existing PSU"""
        if self.collection is None:
            await self._init_collection()
        update_data = psu.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"psu_id": psu_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"PSU with id {psu_id} not found")
        return {"message": "PSU updated successfully"}

    async def delete(self, psu_id: int):
        """Delete a PSU"""
        if self.collection is None:
            await self._init_collection()
        result = await self.collection.delete_one({"psu_id": psu_id})
        if result.deleted_count == 0:
            raise ValueError(f"PSU with id {psu_id} not found")
        return {"message": "PSU deleted successfully", "psu_id": psu_id} 