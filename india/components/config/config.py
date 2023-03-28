import os
from pathlib import Path
import argparse
from pathlib import Path
from typing import Dict

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

APPLICATION = "Observatorio-FCE"
VERSION = "alpha"

def get_args(base: Path) -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dotenv_path",
        type=str,
        default=base,
        help="path where dotenv lives",
    )
    args = vars(parser.parse_args())
    return args


def write_dotenv_example(
    dotenv_directory: Path
    ) -> None:
    """Write an example dotenv file, with expected keys.
    User may modify the values, and add remarks.
    See https://pypi.org/project/python-dotenv/
    """
    with open(dotenv_directory, "w") as target:
        target.write("SECRET_KEY=11111111\n")
        target.write("LOG_TO_STDOUT=YES\n")


def set_environment_variables(application: str, version: str) -> None:
    print("set_environment_variables start")
    base = Path('~', 'Apps', application, version).expanduser()
    args = get_args(base)
    print("set_environment_variables args")
    for key, value in args.items():
        print('    {key:s}: {value:s}')
    base = Path(args["dotenv_path"]).resolve()
    base.mkdir(mode=0o700, parents=True, exist_ok=True)
    print("set_environment_variables dotenv_path", str(base))
    dotenv_path = Path(base, ".env")
    if not dotenv_path.exists():
        write_dotenv_example(dotenv_path)
    load_dotenv(dotenv_path)
    print("set_environment_variables done")


set_environment_variables(APPLICATION, VERSION)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "11235813213455"
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    TWITTER_BEARER_TOKEN = ""
    TWITTER_USERS_FILENAME = ""
    TWITTER_TARGET = ""
    TELEGRAM_TARGET = ""
