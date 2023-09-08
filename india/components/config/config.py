import logging

import argparse
import os
from pathlib import Path
from typing import Dict, Tuple

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-d",
        "--dotenv",
        type=str,
        default=".env",
        help="name of dotenv file",
    )
    args = vars(parser.parse_args())
    return args


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
    def __init__(self, info_home: Path) -> None:
        args = get_args()
        try:
            dotenv = args['dotenv']
        except KeyError:
            dotenv = '.env'
        if not dotenv.startswith('.'):
            dotenv = '.env'
        load_environment_variables(info_home, dotenv)
        self._log_level = os.environ.get("LOG_LEVEL") or "DEBUG"
        telegram_token = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
        twitter_token = os.environ.get("TWITTER_TOKEN") or "112358132134"
        self._authorization_token = {
            "telegram": telegram_token,
            "twitter": twitter_token,
        }

    @property
    def log_level(self) -> int:
        return getattr(logging, self._log_level)

    @property
    def authorization_token(self) -> Dict[str, str]:
        return self._authorization_token
