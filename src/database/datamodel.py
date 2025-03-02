from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List, Optional
from pymongo import MongoClient

client = MongoClient()
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
    ram_id: int = Field(..., description="Ram ID must start with 2 and have 5 digits")
    title: str = Field(..., min_length=1, description="Ram title cannot be empty")
    price: int = Field(..., ge=0, description="Ram price must be non-negative")
    brand: str = Field(..., min_length=1, description="Ram brand cannot be empty")
    memory_type: str = Field(..., min_length=1, description="Ram memory type can not be empty")
    speed: int = Field(..., ge=0, description="Ram speed must be non-negative")
    number_of_DIMMs: int = Field(..., ge=1, description="Number of DIMMs must be greater than 1")
    capacity_per_DIMM: int = Field(..., ge=0, description="Number of DIMMs must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('ram_id')
    def check_id(cls, value):
        if not(20000 < value <= 29999):
            raise ValueError('Ram ID must start with 2 and have 5 digits')
        return value
    
class Mainboard(BaseModel):
    mainboard_id: int = Field(..., description="Mainboard ID must start with 3 and have 5 digits")
    title: str = Field(..., min_length=1, description="Mainboard title cannot be empty")
    price: int = Field(..., ge=0, description="Mainboard price must be non-negative")
    memory_type: str = Field(..., pattern=r"^DDR\d$", description="Mainboaed Memory type shold start with DDR and followed by a single digit")
    size: str = Field(..., min_length=1, description="Mainboard size cannot be empty")
    socket: str = Field(..., min_length=1, description="Mainboard socket cannot be empty")
    brand: str = Field(..., min_length=1, description="Mainboard brand cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('mainboard_id')
    def check_id(cls, value):
        if not(30000 < value <= 39999):
            raise ValueError('Mainboard ID must start with 3 and have 5 digits')
        return value

class SSD(BaseModel):
    ssd_id: int = Field(..., description="SSD ID must start with 42 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="SSD title cannot be empty")
    price: int = Field(..., ge=0, description="SSD price must be non-negative")
    brand: str = Field(..., min_length=1, description="SSD brand cannot be empty")
    size_GB: int = Field(..., ge=0, description="SSD size must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('ssd_id')
    def check_id(cls, value):
        if not(42000 < value <= 42999):
            raise ValueError('SSD ID must start with 42 and have 5 digits')
        return value

class M2(BaseModel):
    m2_id: int = Field(..., description="M2 ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="M2 title cannot be empty")
    price: int = Field(..., ge=0, description="M2 price must be non-negative")
    read: str = Field(..., min_length=1, descrription="M2 read cannot be empty")
    write: str = Field(..., min_length=1, descrription="M2 write cannot be empty")
    brand: str = Field(..., min_length=1, description="M2 brand cannot be empty")
    capacity: int = Field(..., ge=0, description="M2 size must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('m2_id')
    def check_id(cls, value):
        if not(43000 <= value <= 43999):
            raise ValueError('M2 ID must start with 43 and have 5 digits')
        return value
    
class GPU(BaseModel):
    gpu_id: int = Field(..., description="GPU ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="GPU title cannot be empty")
    price: int = Field(..., ge=0, description="GPU price must be non-negative")
    series: str = Field(..., min_length=1, description="GPU series cannot be empty")
    ram_capacity_GB: int = Field(..., ge=0, description="GPU ram capacity must be non-negative")
    brand: str = Field(..., min_length=1, description="GPU brand cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('gpu_id')
    def check_id(cls, value):
        if not(50000 < value <= 59999):
            raise ValueError('GPU ID must start with 5 and have 5 digits')
        return value
    
class Case(BaseModel):
    case_id: int = Field(..., description="Case ID must start with 6 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="Case title cannot be empty")
    price: int = Field(..., ge=0, description="Case price must be non-negative")
    brand: str = Field(..., min_length=1, description="Case brand cannot be empty")
    support_mb: List[str] = Field(..., description="Support Motherboard cannot be empty")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('case_id')
    def check_id(cls, value):
        if not(60000 < value <= 69999):
            raise ValueError('Case ID must start with 6 and have 5 digits')
        return value
    
class PSU(BaseModel):
    psu_id: int = Field(..., description="PSU ID must start with 43 and have 5 digits")
    title: str = Field(..., min_length=1, descrription="PSU title cannot be empty")
    price: int = Field(..., ge=0, description="PSU price must be non-negative")
    Max_Watt: int = Field(..., ge=0, descrription="PSU max watt must be non-negative")
    brand: str = Field(..., min_length=1, description="PSU brand cannot be empty")
    certs: str = Field(..., min_length=1, descrription="PSU certificate cannot be empty")
    grade: int  = None
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('psu_id')
    def check_id(cls, value):
        if not(70000 < value <= 79999):
            raise ValueError('PSU ID must start with 5 and have 5 digits')
        return value
    
# use for updating data

class updateCPU(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    Socket: Optional[str] = None
    brand: Optional[str] = None
    imgUrl: Optional[str] = None

class updateRam(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    brand: Optional[str] = None
    memory_type: Optional[str] = None
    speed: Optional[int] = None
    number_of_DIMMs: Optional[int] = None
    capacity_per_DIMM: Optional[int] = None
    imgUrl: Optional[str] = None
    
class updateMainboard(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    memory_type: Optional[str] = None
    size: Optional[str] = None
    socket: Optional[str] = None
    brand: Optional[str] = None
    imgUrl: Optional[str] = None

class updateSSD(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    brand: Optional[str] = None
    size_GB: Optional[int] = None
    imgUrl: Optional[str] = None

class updateM2(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    read: Optional[str] = None
    write: Optional[str] = None
    brand: Optional[str] = None
    capacity: Optional[int] = None
    imgUrl: Optional[str] = None
    
class updateGPU(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    series: Optional[str] = None
    ram_capacity_GB: Optional[int] = None
    brand: Optional[str] = None
    imgUrl: Optional[str] = None
    
class updateCase(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    brand: Optional[str] = None
    support_mb: Optional[List[str]] = None 
    imgUrl: Optional[str] = None

class updatePSU(BaseModel):
    title: Optional[str] = None
    brand: Optional[str] = None
    price: Optional[float] = None
    Max_Watt: Optional[int] = None
    certs: Optional[str] = None
    imgUrl: Optional[str] = None