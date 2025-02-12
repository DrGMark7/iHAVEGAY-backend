
#. Read json Data from file and then add to database

import os
import json

from pathlib import Path
from typing import List, Union, Dict


def readJsonDataFromFile(Path: Path) -> Dict:
    # Read the data from the json file
    with open('src/database/data.json') as f:
        data = json.load(f)
    return data