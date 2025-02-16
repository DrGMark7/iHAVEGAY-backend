import json
from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List
from pymongo import MongoClient


password = '1q2w3e4r'
client = MongoClient("mongodb+srv://reaw:{0}@test.4hnwy.mongodb.net/".format(password))
print(client.list_database_names())
db = client["mydatabase"]



class CPU(BaseModel):
    cpu_id : int = Field(..., description="CPU ID must start with 1 and have 5 digits")
    title: str = Field(..., min_length=1, description="CPU title cannot be empty")
    price: int = Field(..., ge=0, description="CPU price must be non-negative")
    Socket: str = Field(..., min_length=1, description="CPU socket cannot be empty")
    brand: str = Field(..., min_length=1, description="CPU brand cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('cpu_id')
    def check_cpu_id(cls, value):
        if not (10000 <= value <= 19999):
            raise ValueError('CPU ID must start with 1 and have 5 digits')
        return value


class Ram(BaseModel):
    id: int = Field(..., description="Ram ID must start with 2 and have 5 digits")
    tilte: str = Field(..., min_length=1, description="Ram title cannot be empty")
    price: int = Field(..., ge=0, description="Ram price must be non-negative")
    brand: str = Field(..., min_length=1, description="Ram brand cannot be empty")
    memory_type: str = Field(..., min_length=1, description="Ram memory type can not be empty")
    speed: int = Field(..., ge=0, description="Ram speed must be non-negative")
    num_of_DIMMS: int = Field(..., ge=1, description="Number of DIMMs must be greater than 1")
    cap_per_DIMM: int = Field(..., ge=0, description="Number of DIMMs must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 20000 < value <= 29999:
            raise ValueError('CPU ID must start with 2 and have 5 digits')
        return value
    

class Mainboard(BaseModel):
    id: int = Field(..., description="Mainboard ID must start with 3 and have 5 digits")
    title: str = Field(..., min_length=1, description="Mainboard title cannot be empty")
    price: int = Field(..., ge=0, description="Mainboard price must be non-negative")
    memory_type: str = Field(..., pattern=r"^DDR\d$", description="Mainboaed Memory type shold start with DDR and followed by a single digit")
    size: str = Field(..., min_length=1, description="Mainboard size cannot be empty")
    socket: str = Field(..., min_length=1, description="Mainboard socket cannot be empty")
    brand: str = Field(..., min_length=1, description="Mainboard brand cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 30000 < value <= 39999:
            raise ValueError('Mainboard ID must start with 3 and have 5 digits')
        return value


class SSD(BaseModel):
    id: int = Field(..., description="SSD ID must start with 42 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="SSD title cannot be empty")
    price: int = Field(..., ge=0, description="SSD price must be non-negative")
    brand: str = Field(..., min_length=1, description="SSD brand cannot be empty")
    capacity: int = Field(..., ge=0, description="SSD size must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 42000 < value <= 42999:
            raise ValueError('SSD ID must start with 42 and have 5 digits')
        return value

class M2(BaseModel):
    id: int = Field(..., description="M2 ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="M2 title cannot be empty")
    price: int = Field(..., ge=0, description="M2 price must be non-negative")
    brand: str = Field(..., min_length=1, description="M2 brand cannot be empty")
    capacity: int = Field(..., ge=0, description="M2 size must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 43000 < value <= 43999:
            raise ValueError('M2 ID must start with 42 and have 5 digits')
        return value
    
class GPU(BaseModel):
    id: int = Field(..., description="GPU ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="GPU title cannot be empty")
    price: int = Field(..., ge=0, description="GPU price must be non-negative")
    series: str = Field(..., min_length=1, description="GPU series cannot be empty")
    ram_capacity: int = Field(..., ge=0, description="GPU ram capacity must be non-negative")
    brand: str = Field(..., min_length=1, description="GPU brand cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 50000 < value <= 59999:
            raise ValueError('GPU ID must start with 5 and have 5 digits')
        return value
    
class Case(BaseModel):
    id: int = Field(..., description="Case ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="Case title cannot be empty")
    price: int = Field(..., ge=0, description="Case price must be non-negative")
    brand: str = Field(..., min_length=1, description="Case brand cannot be empty")
    support_mb: List[str] = Field(..., min_length=1, description="Support Motherboard cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 60000 < value <= 69999:
            raise ValueError('Case ID must start with 5 and have 5 digits')
        return value
    
class PSU(BaseModel):
    id: int = Field(..., description="PSU ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="PSU title cannot be empty")
    price: int = Field(..., ge=0, description="PSU price must be non-negative")
    Max_Watt: int = Field(..., ge=0, descrription="PSU max watt must be non-negative")
    brand: str = Field(..., min_length=1, description="PSU brand cannot be empty")
    cert: str = Field(..., min_length=1, descrription="PSU certificate cannot be empty")
    grade: int  = Field(..., ge=0, description="PSU grade must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('id')
    def check_id(cls, value):
        if 70000 < value <= 79999:
            raise ValueError('PSU ID must start with 5 and have 5 digits')
        return value

class HardwareManager:
    def __init__(self):
        self.CPU_collection = db['CPUs']
        self.Ram_collection = db['Rams']
        self.Mainboard_collection = db['Mainboards']
        self.SSD_collection = db['SSDs']
        self.M2_collection = db['M2s']
        self.GPU_collection = db['GPUs']
        self.Case_collection = db['Cases']
        self.PSU_collection = db['PSUs']
    
    def add_cpu(self, cpu_file_path):
        try:
            with open(cpu_file_path, "r", encoding="utf-8") as file:
                cpu_data = json.load(file)
        except Exception as e:
            print(f"Error reading file {cpu_file_path}: {e}")
            return

        valid_cpus = []

        for cpu in cpu_data:
            if isinstance(cpu['price'],str):
                cpu['price'] = int(cpu['price'].replace(',', ''))
            try:
                validated_cpu = CPU(**cpu)
                valid_cpus.append(validated_cpu.model_dump(by_alias=True))
            except Exception as e:
                print(f"Invalid data: {cpu} - Error: {e}")

        if valid_cpus:
            self.CPU_collection.insert_many(valid_cpus)
            print(f"Inserted {len(valid_cpus)} cpus into MongoDB.")
