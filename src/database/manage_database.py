
#. Read json Data from file and then add to database
import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Union, Dict
from pymongo import MongoClient
from config import BaseConfig
from src.database.database import Database
from datamodel import CPU, Ram, Mainboard, SSD, M2, GPU, Case, PSU

class HardwareManager:
    def __init__(self):
        self.CPU_collection = Database.get_collection('CPUs')
        self.Ram_collection = Database.get_collection('Rams')
        self.Mainboard_collection = Database.get_collection('Mainboards')
        self.SSD_collection = Database.get_collection('SSDs')
        self.M2_collection = Database.get_collection('M2s')
        self.GPU_collection = Database.get_collection('GPUs')
        self.Case_collection = Database.get_collection('Cases')
        self.PSU_collection = Database.get_collection('PSUs')

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
