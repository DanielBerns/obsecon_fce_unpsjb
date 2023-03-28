from collections import defaultdict, Counter
from contextlib import contextmanager
import datetime
import json
import os
from pathlib import Path
from typing import List, Dict, Union
from shutil import rmtree


import pandas as pd


indentation = '    '


def get_timestamp() -> str:
    now = datetime.datetime.now()
    timestamp = ''.join([f'{now.year:4d}{now.month:02d}',
                         f'{now.day:02d}{now.hour:02d}',
                         f'{now.minute:02d}',
                         f'{now.second:02d}'])
    return timestamp


def save_json(data_json: Path, data: Dict) -> None:
    with open(data_json, 'w') as target:
        json.dump(data, target)


def load_json(data_json: Path) -> Dict:
    data = None
    with open(data_json, 'r') as source:
        data = json.load(source)
    return data


def readlines(textfile: Path) -> List[str]:
    lines = None
    with open(textfile, 'r') as source:
        lines = [line[:-1] for line in source]
    return lines


def get_directory(base: Path) -> Path:
    directory = Path(base).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory

def get_container(base: Path, identifier: str):
    return get_directory(Path(base, identifier))

def get_resource_identifier(base: Path, name: str, suffix: str) -> Path:
    return get_directory(Path(base, name)).with_suffix(suffix)

def remove_directory(base: Path) -> None:
    rmtree(base)

