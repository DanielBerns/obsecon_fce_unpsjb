import logging

import argparse
import os
from pathlib import Path
from typing import Dict, Tuple

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv


CONTEXT = "India"
VERSION = "alpha"


default_root_folder = str(Path('~', 'Apps').expanduser())


def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--root",
        type=str,
        default=default_root_folder,
        help="root folder",
    )
    parser.add_argument(
        "-i",
        "--instance",
        type=str,
        default="Test",
        help="instance name",
    )
    parser.add_argument(
        "-d",
        "--dotenv",
        type=str,
        default=".env",
        help="name of dotenv file",
    )
    args = vars(parser.parse_args())
    return args


def get_root_instance_dotenv(args: Dict[str, str]) -> Tuple[str, str, str]:
    root = str(Path(args["root"]).expanduser())
    instance = args["instance"]
    dotenv = args["dotenv"]
    return root, instance, dotenv


def get_home(root: str,
             context: str,
             version: str,
             instance: str,
             ) -> Path:
    home = Path(root, context, version, instance).expanduser()
    home.mkdir(mode=0o700, parents=True, exist_ok=True)    
    return home


def write_dotenv(dotenv_full_filename: Path) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_full_filename, "w") as target:
        target.write("LOG_STDOUT=YES\n")
        target.write("LOG_STDOUT_LEVEL=DEBUG\n")
        target.write("LOG_FILE_LEVEL=INFO\n")        
        target.write("TWITTER_TOKEN=112358132134\n")        
        target.write("TELEGRAM_TOKEN=112358132134\n")


def load_environment_variables(home: str, dotenv: str) -> None:
    dotenv_full_filename = Path(home, dotenv)
    if not dotenv_full_filename.exists():
        write_dotenv(dotenv_full_filename)
    load_dotenv(dotenv_full_filename)
    
    
class Config:
    def __init__(self):
        args = get_args()
        root, instance, dotenv = get_root_instance_dotenv(args)
        home = get_home(root, CONTEXT, VERSION, instance)        
        load_environment_variables(home, dotenv)
        self._home = home
        self._log_stdout = os.environ.get("LOG_STDOUT") or "YES"
        self._log_stdout_level = os.environ.get("LOG_STDOUT_LEVEL") or "DEBUG"
        self._log_filename = "logs.txt" 
        self._log_file_level = os.environ.get("LOG_FILE_LEVEL") or "INFO"        
        telegram_token = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
        twitter_token = os.environ.get("TWITTER_TOKEN") or "112358132134"
        self._authorization_token = {"telegram": telegram_token, "twitter": twitter_token}

    @property
    def home(self):
        return self._home

    @property
    def log_stdout(self):
        return self._log_stdout
    
    @property
    def log_stdout_level(self) -> int:
        return getattr(logging, self._log_stdout_level)

    @property
    def log_file(self) -> str:
        return self._log_file
    
    @property
    def log_file_level(self) -> int:
        return getattr(logging, self._log_file_level)

    @property
    def log_filename(self) -> str:
        return self._log_filename

    @property    
    def authorization_token(self) -> Dict[str, str]:
        return self._authorization_token
        
