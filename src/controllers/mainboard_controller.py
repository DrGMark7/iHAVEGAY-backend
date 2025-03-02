from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import Mainboard, UpdateMainboard
from src.services.hardware_service import HardwareService

class MainboardController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('Mainboards')

    async def get_all(self):
        """Get all Mainboards from database"""
        if not self.collection:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, mainboard_id: int):
        """Get a Mainboard by its ID"""
        if not self.collection:
            await self._init_collection()
        mainboard = await self.collection.find_one({"mainboard_id": mainboard_id}, {"_id": 0})
        if not mainboard:
            raise ValueError(f"Mainboard with id {mainboard_id} not found")
        return mainboard

    async def create(self, mainboard: Mainboard):
        """Create a new Mainboard"""
        if not self.collection:
            await self._init_collection()
        mainboard_dict = mainboard.model_dump(exclude_none=True)
        result = await self.collection.insert_one(mainboard_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert Mainboard")
        return {"message": "Mainboard added successfully", "id": str(result.inserted_id)}

    async def update(self, mainboard_id: int, mainboard: UpdateMainboard):
        """Update an existing Mainboard"""
        if not self.collection:
            await self._init_collection()
        update_data = mainboard.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"mainboard_id": mainboard_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"Mainboard with id {mainboard_id} not found")
        return {"message": "Mainboard updated successfully"}

    async def delete(self, mainboard_id: int):
        """Delete a Mainboard"""
        if not self.collection:
            await self._init_collection()
        result = await self.collection.delete_one({"mainboard_id": mainboard_id})
        if result.deleted_count == 0:
            raise ValueError(f"Mainboard with id {mainboard_id} not found")
        return {"message": "Mainboard deleted successfully", "mainboard_id": mainboard_id}
