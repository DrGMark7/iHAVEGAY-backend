from src.database.database import Database

class HardwareService:
    def __init__(self):
        self.db = Database

    async def validate_hardware_exists(self, collection_name: str, hardware_id: int, id_field: str):
        collection = self.db.get_collection(collection_name)
        hardware = await collection.find_one({id_field: hardware_id})
        return hardware is not None

    async def get_compatible_parts(self, cpu_socket: str):
        
        mainboard_collection = self.db.get_collection('Mainboards')
        compatible_mainboards = await mainboard_collection.find(
            {"socket": cpu_socket},
            {"_id": 0}
        ).to_list(length=None)
        return compatible_mainboards 