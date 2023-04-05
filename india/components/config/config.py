import os
from pathlib import Path
import argparse
from pathlib import Path
from typing import Dict
from components.core import FileSystem

# https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

APPLICATION = os.environ.get("APPLICATION") or "India"
VERSION = os.environ.get("VERSION") or "alpha"
INSTANCE = os.environ.get("INSTANCE") or "Test"

def get_args() -> Dict[str, str]:
    """Construct the argument parser and parse the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--log_to_stdout",
        type=str,
        choices=["no", "yes"],
        default="yes",
        help="log to stdout? [yes] or no",
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
        target.write("LOG_TO_STDOUT=yes\n")


def set_environment_variables(fs: FileSystem) -> None:
    print("set_environment_variables start")
    args = get_args()
    print("  args")
    for key, value in args.items():
        print(f"    {key:s}: {str(value):s}")
    dotenv_full_filename = Path(fs.home, ".env")
    if not dotenv_full_filename.exists():
        print(f"  dotenv_full_filename:", str(dotenv_full_filename))
        write_dotenv_example(dotenv_full_filename)
    load_dotenv(dotenv_full_filename)
    print("set_environment_variables done")


fs = FileSystem(APPLICATION, VERSION, INSTANCE)
set_environment_variables(fs)


class Config:
    LOG_TO_STDOUT = os.environ.get("log_to_stdout")
    FILESYSTEM = fs
    TWITTER_USERS_FILENAME = "users.json"
