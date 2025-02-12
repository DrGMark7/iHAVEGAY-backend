
#. Read json Data from file and then add to database

import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Union, Dict
from pymongo import MongoClient

from config import BaseConfig

def add_data_to_database():
    
    config = BaseConfig()
    host = config['Database']['Host']
    port = config['Database']['Port']
    client = MongoClient(host, port)
    
    for data in DataParser().read_data():
        client.insert(data)
