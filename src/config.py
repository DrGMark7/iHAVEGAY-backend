import yaml
import logging
from pathlib import Path
from typing import Dict, Any

def loadConfig() -> Dict:
    try:
        with open('config.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data
    except FileNotFoundError:
        logging.error("Config file not found")
        return None

class BaseConfig:
    def __init__(self, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.config = loadConfig()

    """
    __getitem__ method is used to access the item using the key.
    Returns the value of the key Any String
    """
    def __getitem__(self, key) -> Any:
        try:
            return self.config[key]
        except KeyError:
            logging.error(f"Key {key} not found in config") 
            return None
    
    def __setitem__(self, key, value):
        self.config[key] = value

    def __delitem__(self, key):
        del self.config[key]

    def show(self) -> None:
        for key, value in self.config.items():
            print(f"[Base Config] {key}")
            for k, v in value.items():
                print(f'\t{k}: {v}')
    

