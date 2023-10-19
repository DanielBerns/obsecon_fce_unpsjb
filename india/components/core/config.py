import logging

from argparse import ArgumentParser
import os
from pathlib import Path
from typing import Dict, Tuple

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

class CLIConfig:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()

    @property
    def parser(self) -> ArgumentParser:
        return self._parser

    @property
    def args(self) -> Dict[str, str]:
        value = vars(parser.parse_args())
        return {str(k): str(v) for k, v in value.items()}
    
    def add_arguments(self) -> None:
        self.parser.add_argument(
            "-d",
            "--dotenv",
            type=str,
            default=".env",
            help="name of dotenv file",
        )
        self.parser.add_argument(
            "-m",
            "--mode",
            choices=["test", "live"],
            type=str,
            default="test", required=False
            help="how to run? test or live",
        )


def write_dotenv(dotenv_full_filename: Path) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_full_filename, "w") as target:
        target.write("LOG_LEVEL=DEBUG\n")
        target.write("TELEGRAM_TOKEN=112358132134\n")


def load_environment_variables(home: str, dotenv: str) -> None:
    dotenv_full_filename = Path(home, dotenv)
    if not dotenv_full_filename.exists():
        write_dotenv(dotenv_full_filename)
    load_dotenv(dotenv_full_filename)


class Config:
    def __init__(self, home: Path, args: Dict[str, str]) -> None:
        try:
            dotenv = args["dotenv"]
        except KeyError:
            dotenv = ".env"
        if not dotenv.startswith("."):
            dotenv = ".env"
        load_environment_variables(home, dotenv)
        self._log_level = os.environ.get("LOG_LEVEL") or "DEBUG"
        telegram_token = os.environ.get("TELEGRAM_TOKEN") or "112358132134"
        self._authorization_token = {
            "telegram": telegram_token,
        }
        mode = args["mode"]
        self._mode = mode if mode in ["test", "live"] else "test"

    @property
    def log_level(self) -> int:
        return getattr(logging, self._log_level)

    @property
    def authorization_token(self) -> Dict[str, str]:
        return self._authorization_token

    @property
    def mode(self) -> str:
        return self._mode
