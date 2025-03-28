from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import Case, UpdateCase
from src.services.hardware_service import HardwareService

class CaseController:
    def __init__(self):
        self.collection = None
        self._init_collection()
        self.service = HardwareService()

    async def _init_collection(self):
        """Initialize MongoDB collection asynchronously"""
        self.collection = await Database.get_collection('Cases')

    async def get_all(self):
        """Get all Cases from database"""
        if self.collection is None:
            await self._init_collection()
        cursor = self.collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_by_id(self, case_id: int):
        """Get a Case by its ID"""
        if self.collection is None:
            await self._init_collection()
        case = await self.collection.find_one({"case_id": case_id}, {"_id": 0})
        if not case:
            raise ValueError(f"Case with id {case_id} not found")
        return case

    async def create(self, case: Case):
        """Create a new Case"""
        if self.collection is None:
            await self._init_collection()
        case_dict = case.model_dump(exclude_none=True)
        result = await self.collection.insert_one(case_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert Case")
        return {"message": "Case added successfully", "id": str(result.inserted_id)}

    async def update(self, case_id: int, case: UpdateCase):
        """Update an existing Case"""
        if self.collection is None:
            await self._init_collection()
        update_data = case.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.collection.update_one(
            {"case_id": case_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"Case with id {case_id} not found")
        return {"message": "Case updated successfully"}

    async def delete(self, case_id: int):
        """Delete a Case"""
        if self.collection is None:
            await self._init_collection()
        result = await self.collection.delete_one({"case_id": case_id})
        if result.deleted_count == 0:
            raise ValueError(f"Case with id {case_id} not found")
        return {"message": "Case deleted successfully", "case_id": case_id}
