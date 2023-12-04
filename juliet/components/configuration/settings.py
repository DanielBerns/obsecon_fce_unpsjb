import logging

import os

from pathlib import Path
from typing import Dict, Tuple, Callable

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from components.helpers import get_home


class Constants:
    INFO: str = "Info"
    SOFTWARE: str = "Software"
    PROJECT: str = "athena"
    VERSION: str = "juliet"

        
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
    def load_dotenv(
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
        project: str,
        version: str,
        mode: str, 
        application: str, 
        dotenv: str
        ) -> None:
        log_level_key: str = f"{application.upper():s}_LOG_LEVEL"        
        telegram_token_key: str = f"{application.upper():s}_TELEGRAM_TOKEN"
        get_default_dotenv = lambda : {log_level_key: "DEBUG", telegram_token_key: "112358132134"}
       
        info_home = get_home(
            Settings.info_root, 
            project, version,
            mode, application)
        software_home = get_home(
            Settings.software_root, 
            project, version,
            mode, application)
        
        Settings.load_dotenv(info_home, dotenv, get_default_dotenv)
        
        log_level: str = os.environ.get(log_level_key) or "DEBUG"
        telegram_token: str = os.environ.get(telegram_token_key) or "112358132134"
            
        return {"info_home": str(info_home),
                "software_home": str(software_home),
                "log_level": log_level,
                "telegram_token": telegram_token}
