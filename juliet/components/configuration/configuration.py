import logging

import argparse
import os
from pathlib import Path
from typing import Dict, Tuple

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

CONTEXT = "observatorio_fce_unpsjb"
VERSION = "juliet"

default_info_root = str(Path('~', 'Info').expanduser())
default_apps_root = str(Path('~', 'Apps').expanduser())

class CLI:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()
        
    @property
    def parser(self) -> argparse.ArgumentParser:
        return self._parser
    
    def arguments(self) -> Dict[str, str]:
        return vars(self.parser.parse_args())


def get_home(root: str,
             context: str,
             version: str,
             instance: str,
             ) -> Path:
    home = Path(root, context, version, instance).expanduser()
    home.mkdir(mode=0o700, parents=True, exist_ok=True)    
    return home


def write_dotenv(
    dotenv_full_filename: Path,
    parameters: Dict[str, str]) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_full_filename, "w") as target:
        for key, value in parameters.items():
            target.write(f"{key:s}={value:s}\n")


def load_environment_variables(home: str, dotenv: str) -> None:
    dotenv_resource = Path(home, dotenv)
    if not dotenv_resource.exists():
        write_dotenv(dotenv_resource, {"instance": "test", "dotenv": ".env"})
    load_dotenv(dotenv_full_filename)


def get_parameters(instance: str, dotenv: str):
    application_home = get_home(default_apps_root, CONTEXT, VERSION, instance)
    info_home = get_home(default_info_root, CONTEXT, VERSION, instance)        
    load_environment_variables(application_home, dotenv)
    log_level = os.environ.get("LOG_LEVEL") or "DEBUG"        
    telegram_token = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
    twitter_token = os.environ.get("TWITTER_TOKEN") or "112358132134"
    return {"application_home": application_home,
            "info_home": info_home
            "log_level": log_level,
            "telegram_token": telegram_token,
            "twitter_token": twitter_token}
