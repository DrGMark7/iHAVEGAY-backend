from fastapi import HTTPException
from src.database.database import Database
from src.models.hardware_models import SSD, M2, UpdateSSD, UpdateM2
from src.services.hardware_service import HardwareService

class StorageController:
    def __init__(self):
        self.ssd_collection = None
        self.m2_collection = None
        self._init_collections()
        self.service = HardwareService()

    async def _init_collections(self):
        """Initialize MongoDB collections asynchronously"""
        self.ssd_collection = await Database.get_collection('SSDs')
        self.m2_collection = await Database.get_collection('M2s')

    # SSD Methods
    async def get_all_ssds(self):
        """Get all SSDs from database"""
        if self.ssd_collection is None:
            await self._init_collections()
        cursor = self.ssd_collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_ssd_by_id(self, ssd_id: int):
        """Get an SSD by its ID"""
        if self.ssd_collection is None:
            await self._init_collections()
        ssd = await self.ssd_collection.find_one({"ssd_id": ssd_id}, {"_id": 0})
        if not ssd:
            raise ValueError(f"SSD with id {ssd_id} not found")
        return ssd

    async def create_ssd(self, ssd: SSD):
        """Create a new SSD"""
        if self.ssd_collection is None:
            await self._init_collections()
        ssd_dict = ssd.model_dump(exclude_none=True)
        result = await self.ssd_collection.insert_one(ssd_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert SSD")
        return {"message": "SSD added successfully", "id": str(result.inserted_id)}

    async def update_ssd(self, ssd_id: int, ssd: UpdateSSD):
        """Update an existing SSD"""
        if self.ssd_collection is None:
            await self._init_collections()
        update_data = ssd.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.ssd_collection.update_one(
            {"ssd_id": ssd_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"SSD with id {ssd_id} not found")
        return {"message": "SSD updated successfully"}

    async def delete_ssd(self, ssd_id: int):
        """Delete an SSD"""
        if self.ssd_collection is None:
            await self._init_collections()
        result = await self.ssd_collection.delete_one({"ssd_id": ssd_id})
        if result.deleted_count == 0:
            raise ValueError(f"SSD with id {ssd_id} not found")
        return {"message": "SSD deleted successfully", "ssd_id": ssd_id}

    # M.2 Methods
    async def get_all_m2s(self):
        """Get all M.2 drives from database"""
        if self.m2_collection is None:
            await self._init_collections()
        cursor = self.m2_collection.find({}, {"_id": 0})
        return await cursor.to_list(length=None)

    async def get_m2_by_id(self, m2_id: int):
        """Get an M.2 drive by its ID"""
        if self.m2_collection is None:
            await self._init_collections()
        m2 = await self.m2_collection.find_one({"m2_id": m2_id}, {"_id": 0})
        if not m2:
            raise ValueError(f"M.2 drive with id {m2_id} not found")
        return m2

    async def create_m2(self, m2: M2):
        """Create a new M.2 drive"""
        if self.m2_collection is None:
            await self._init_collections()
        m2_dict = m2.model_dump(exclude_none=True)
        result = await self.m2_collection.insert_one(m2_dict)
        if not result.inserted_id:
            raise ValueError("Failed to insert M.2 drive")
        return {"message": "M.2 drive added successfully", "id": str(result.inserted_id)}

    async def update_m2(self, m2_id: int, m2: UpdateM2):
        """Update an existing M.2 drive"""
        if self.m2_collection is None:
            await self._init_collections()
        update_data = m2.model_dump(exclude_none=True)
        if not update_data:
            raise ValueError("No valid update data provided")
        
        result = await self.m2_collection.update_one(
            {"m2_id": m2_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise ValueError(f"M.2 drive with id {m2_id} not found")
        return {"message": "M.2 drive updated successfully"}

    async def delete_m2(self, m2_id: int):
        """Delete an M.2 drive"""
        if self.m2_collection is None:
            await self._init_collections()
        result = await self.m2_collection.delete_one({"m2_id": m2_id})
        if result.deleted_count == 0:
            raise ValueError(f"M.2 drive with id {m2_id} not found")
        return {"message": "M.2 drive deleted successfully", "m2_id": m2_id}
