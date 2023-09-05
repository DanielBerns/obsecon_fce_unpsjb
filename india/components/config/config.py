import logging

import argparse
import os
from pathlib import Path
from typing import Dict, Tuple

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

CONTEXT = "observatorio_fce_unpsjb"
VERSION = "india"

info_home = str(Path("~", "Info").expanduser())
apps_home = str(Path("~", "Apps").expanduser())


def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--instance",
        type=str,
        default="test",
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


def get_instance_dotenv(args: Dict[str, str]) -> Tuple[str, str]:
    instance = args["instance"]
    dotenv = args["dotenv"]
    return instance, dotenv


def get_info_home(
    context: str,
    version: str,
    instance: str,
) -> Path:
    home = Path(info_home, context, version, instance).expanduser()
    home.mkdir(mode=0o700, parents=True, exist_ok=True)
    return home


def get_application_home(
    context: str,
    version: str,
    instance: str,
) -> Path:
    home = Path(apps_home, context, version, instance).expanduser()
    home.mkdir(mode=0o700, parents=True, exist_ok=True)
    return home


def write_dotenv(dotenv_full_filename: Path) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_full_filename, "w") as target:
        target.write("LOG_LEVEL=DEBUG\n")
        target.write("TWITTER_TOKEN=112358132134\n")
        target.write("TELEGRAM_TOKEN=112358132134\n")


def load_environment_variables(home: str, dotenv: str) -> None:
    dotenv_full_filename = Path(home, dotenv)
    if not dotenv_full_filename.exists():
        write_dotenv(dotenv_full_filename)
    load_dotenv(dotenv_full_filename)


class Config:
    def __init__(self, context: str, version: str, instance: str):
        args = get_args()
        instance, dotenv = get_instance_dotenv(args)
        application_home = get_application_home(context, version, instance)
        info_home = get_info_home(context, version, instance)
        load_environment_variables(info_home, dotenv)
        self._application_home = application_home
        self._info_home = info_home

        self._log_level = os.environ.get("LOG_LEVEL") or "DEBUG"
        telegram_token = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
        twitter_token = os.environ.get("TWITTER_TOKEN") or "112358132134"
        self._authorization_token = {
            "telegram": telegram_token,
            "twitter": twitter_token,
        }

    @property
    def info_home(self) -> Path:
        return self._info_home

    @property
    def application_home(self) -> Path:
        return self._application_home

    @property
    def log_level(self) -> int:
        return getattr(logging, self._log_level)

    @property
    def authorization_token(self) -> Dict[str, str]:
        return self._authorization_token
