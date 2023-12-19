import logging

import os

from pathlib import Path
from typing import Dict, Tuple, Callable

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from components.helpers import get_home


class Constants:
    INFO: str = "Info"
    SOFTWARE: str = "Apps"
    PROJECT: str = "observatorio_fce_unpsjb"
    VERSION: str = "india"

        
class Settings:

    info_root: str = str(Path('~', Constants.INFO).expanduser())
    software_root: str = str(Path('~', Constants.SOFTWARE).expanduser())
    
    @staticmethod
    def write_dotenv(
        dotenv_resource: Path,
        parameters: Dict[str, str]) -> None:
        """Write an example dotenv file, with expected keys.
        User may modify the values, and add remarks.
        See https://pypi.org/project/python-dotenv/
        """
        with open(dotenv_resource, "w") as target:
            target.write("# settings\n")
            for key, value in parameters.items():
                target.write(f"{key:s}={value:s}\n")

    @staticmethod
    def read_dotenv(
        home: str, 
        dotenv: str,
        default_dotenv: Callable[[], Dict[str, str]]
        ) -> None:
        """Load key value pairs from a text file 
           and set some environment variables.
           If dotenv_resource doesnt exists, 
              create it with default values from a callable
        """
        dotenv_resource = Path(home, dotenv)
        if not dotenv_resource.exists():
            Settings.write_dotenv(dotenv_resource, default_dotenv())
        load_dotenv(dotenv_resource)
    
    @staticmethod    
    def build(
        identifier: str, 
        mode: str, 
        dotenv: str
        ) -> Dict[str, str]:
        
        log_level_key: str = f"{identifier.upper():s}_LOG_LEVEL"
        get_default_dotenv = lambda : {log_level_key: "DEBUG"}
       
        info_home = get_home(
            Settings.info_root, 
            Constants.PROJECT, Constants.VERSION,
            mode, identifier)
        
        software_home = get_home(
            Settings.software_root, 
            Constants.PROJECT, Constants.VERSION,
            mode, identifier)
        
        Settings.read_dotenv(info_home, dotenv, get_default_dotenv)
        
        log_level: str = os.environ.get(log_level_key) or "DEBUG"
            
        return {"mode": mode,
                "identifier": identifier,
                "info_home": str(info_home),
                "software_home": str(software_home),
                "log_level": log_level
                }
