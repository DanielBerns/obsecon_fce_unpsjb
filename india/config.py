import logging

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Dict

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

from components.core import FileSystem

APPLICATION = "India"
VERSION = "alpha"


class ConfigError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

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


def write_dotenv_example(
    dotenv_full_filename: Path
    ) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_full_filename, "w") as target:
        target.write(f"ROOT={default_root_folder:s}\n")        
        target.write("INSTANCE=Test\n")        
        target.write("LOG_TARGET=STDOUT\n")
        target.write("LOG_LEVEL=INFO\n")        
        target.write("TWITTER_BEARER_TOKEN=112358132134\n")        
        target.write("TELEGRAM_TOKEN=112358132134\n")


def set_environment_variables() -> None:
    print("set_environment_variables start")
    args = get_args()
    print(":  CLI arguments")    
    for key, value in args.items():
        print(f":    args[{key:s}]: {str(value):s}")
    root = str(Path(args["root"]).expanduser())
    instance = args["instance"]
    dotenv = args["dotenv"]
    home = FileSystem.get_home(root, APPLICATION, VERSION, instance)
    home.mkdir(mode=0o700, parents=True, exist_ok=True)
    dotenv_full_filename = Path(home, dotenv)
    print(f":                  home: {str(home):s}")
    print(f":  dotenv_full_filename: {str(dotenv_full_filename):s}")            
    if not dotenv_full_filename.exists():
        print(":  Creating dotenv with default values")        
        write_dotenv_example(dotenv_full_filename)
    print(":  Loading dotenv")                
    load_dotenv(dotenv_full_filename)
    print("set_environment_variables done")


set_environment_variables()

    
@dataclass(frozen=True)
class Config:
    ROOT = os.environ.get("ROOT") or str(Path('~', 'Apps'))
    INSTANCE = os.environ.get("INSTANCE") or "Test"
    LOG_TARGET = os.environ.get("LOG_TARGET") or "STDOUT"
    LOG_LEVEL = os.environ.get("LOG_LEVEL") or "DEBUG"
    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
    TWITTER_BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN") or "112358132134"

    @staticmethod
    def get_log_level() -> int:
        LOG_LEVELS = {"CRITICAL": logging.CRITICAL,
              "ERROR": logging.ERROR,
              "WARNING": logging.WARNING,
              "INFO": logging.INFO,
              "DEBUG": logging.DEBUG,
              "NOTSET": logging.NOTSET}        
        return LOG_LEVELS.get(Config.LOG_LEVEL, "DEBUG")
