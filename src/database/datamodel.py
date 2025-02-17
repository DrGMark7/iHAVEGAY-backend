import json
from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import List
from pymongo import MongoClient

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
    support_mb: List[str] = Field(..., min_length=1, description="Support Motherboard cannot be empty")
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
    grade: int  = Field(..., ge=0, description="PSU grade must be non-negative")
    imgUrl: str = Field(..., description="Official website URL")

    @field_validator('psu_id')
    def check_id(cls, value):
        if not(70000 < value <= 79999):
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
                valid_cpus.append(validated_cpu.model_dump())
            except Exception as e:
                print(f"Invalid data: {cpu} - Error: {e}")

        if valid_cpus:
            self.CPU_collection.insert_many(valid_cpus)
            print(f"Inserted {len(valid_cpus)} cpus into MongoDB.")
    
    def add_ram(self, ram_file_path):
        try:
            with open(ram_file_path, "r", encoding="utf-8") as file:
                ram_data =json.load(file)
        except Exception as e:
            print(f"Error reading file {ram_file_path}: {e}")

        valid_rams = []

        for ram in ram_data:
            try:
                if isinstance(ram['price'],str):
                    ram['price'] = int(ram['price'].replace(',', ''))
                    try:
                        ram['speed'] = int(ram['speed'])
                        ram['number_of_DIMMs'] = int(ram['number_of_DIMMs'])
                        ram['capacity_per_DIMM'] = int(ram['capacity_per_DIMM'])
                    except ValueError as e:
                        raise ValueError(f"Invalid value in fields: speed, number_of_DIMMs, capacity_per_DIMM - Error: {e}")
                validated_ram = Ram(**ram)
                valid_rams.append(validated_ram.model_dump())
            except Exception as e:
                print(f"Invalid data: {ram} - Error: {e}")

        if valid_rams:
            self.Ram_collection.insert_many(valid_rams)
            print(f"Inserted {len(valid_rams)} rams into MongoDB.")
    
    def add_mainboard(self, mainboard_file_path):
        try:
            with open(mainboard_file_path, "r", encoding="utf-8") as file:
                mainboard_data = json.load(file)
        except Exception as e:
            print(f"Error reading file {mainboard_file_path}: {e}")

        valid_mbs = []

        for mb in mainboard_data:
            if isinstance(mb['price'],str):
                mb['price'] = int(mb['price'].replace(',', ''))
            try:
                validated_mb = Mainboard(**mb)
                valid_mbs.append(validated_mb.model_dump())
            except Exception as e:
                print(f"Invalid data: {mb} - Error: {e}")

        if valid_mbs:
            self.Mainboard_collection.insert_many(valid_mbs)
            print(f"Inserted {len(valid_mbs)} Mainboard into MongoDB.")

    def add_ssd(self, ssd_file_path):
        try:
            with open(ssd_file_path, 'r', encoding="utf-8") as file:
                ssd_data = json.load(file)
        except Exception as e:
            print(f"Error reading file {ssd_file_path}: {e}")

        
        valid_ssds = []

        for ssd in ssd_data:
            if isinstance(ssd['price'], str):
                ssd['price'] = int(ssd['price'].replace(',', ''))

            try:
                validated_ssd = SSD(**ssd)
                valid_ssds.append(validated_ssd.model_dump())
            except Exception as e:
                print(f"Invalid data: {ssd} - Error: {e}")

        if valid_ssds:
            self.SSD_collection.insert_many(valid_ssds)
            print(f"Inserted {len(valid_ssds)} SSD into MongoDB.")

    def add_m2(self, m2_file_path):
            try:
                with open(m2_file_path, 'r', encoding="utf-8") as file:
                    m2_data = json.load(file)
            except Exception as e:
                print(f"Error reading file {m2_file_path}: {e}")

            
            valid_m2s = []

            for m2 in m2_data:
                if isinstance(m2['price'], str):
                    m2['price'] = int(m2['price'].replace(',', ''))
                    m2['capacity'] = int(float(m2['capacity']))
                try:
                    validated_m2 = M2(**m2)
                    valid_m2s.append(validated_m2.model_dump())
                except Exception as e:
                    print(f"Invalid data: {m2} - Error: {e}")

            if valid_m2s:
                self.M2_collection.insert_many(valid_m2s)
                print(f"Inserted {len(valid_m2s)} M2 into MongoDB.")

    def add_gpu(self, gpu_file_path):
            try:
                with open(gpu_file_path, 'r', encoding="utf-8") as file:
                    gpu_data = json.load(file)
            except Exception as e:
                print(f"Error reading file {gpu_file_path}: {e}")

            
            valid_gpus = []

            for gpu in gpu_data:
                if isinstance(gpu['price'], str):
                    gpu['price'] = int(gpu['price'].replace(',', ''))
                try:
                    validated_gpu = GPU(**gpu)
                    valid_gpus.append(validated_gpu.model_dump())
                except Exception as e:
                    print(f"Invalid data: {gpu} - Error: {e}")

            if valid_gpus:
                self.GPU_collection.insert_many(valid_gpus)
                print(f"Inserted {len(valid_gpus)} GPU into MongoDB.")

    def add_case(self, case_file_path):
        try:
            with open(case_file_path, 'r', encoding="utf-8") as file:
                case_data = json.load(file)
        except Exception as e:
            print(f"Error reading file {case_file_path}: {e}")

        
        valid_cases = []

        for case in case_data:
            if isinstance(case['price'], str):
                case['price'] = int(case['price'].replace(',', ''))
            try:
                case['support_mb'] = case['support_mb'].split(' , ')
            except Exception as e:
                print(f"Unexpected error: {e} - case: {case}")
            try:
                validated_case = Case(**case)
                valid_cases.append(validated_case.model_dump())
            except Exception as e:
                print(f"Invalid data: {case} - Error: {e}")

        if valid_cases:
            self.Case_collection.insert_many(valid_cases)
            print(f"Inserted {len(valid_cases)} case into MongoDB.")

    def add_psu(self, psu_file_path):
        try:
            with open(psu_file_path, 'r', encoding="utf-8") as file:
                psu_data = json.load(file)
        except Exception as e:
            print(f"Error reading file {psu_file_path}: {e}")

        
        valid_psus = []

        for psu in psu_data:
            if isinstance(psu['price'], str):
                psu['price'] = int(psu['price'].replace(',', ''))
            psu['Max_Watt'] = int(psu['Max_Watt'].split(' ')[0])
            try:
                validated_psu = PSU(**psu)
                valid_psus.append(validated_psu.model_dump())
            except Exception as e:
                print(f"Invalid data: {psu} - Error: {e}")

        if valid_psus:
            self.PSU_collection.insert_many(valid_psus)
            print(f"Inserted {len(valid_psus)} Psu into MongoDB.")
