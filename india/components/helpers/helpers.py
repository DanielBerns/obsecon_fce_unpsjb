from collections import defaultdict, Counter
from contextlib import contextmanager
import datetime
import json
import os
from pathlib import Path
from typing import List, Dict, Union
from shutil import rmtree


indentation = "    "


def get_timestamp() -> str:
    now = datetime.datetime.now()
    timestamp = "".join(
        [
            f"{now.year:4d}{now.month:02d}",
            f"{now.day:02d}{now.hour:02d}",
            f"{now.minute:02d}",
            f"{now.second:02d}",
        ]
    )
    return timestamp


def save_json(data_json: Path, data: Dict) -> None:
    with open(data_json, "w") as target:
        json.dump(data, target)


def load_json(data_json: Path) -> Dict[str, str]:
    data = None
    with open(data_json, "r") as source:
        data = json.load(source)
    return data

def read_text(source: Path) -> str:
    # get text from utf-8 encoded file
    with open(source, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def read_text_lines(source: Path) -> List[str]:
    with open(source, "r") as f:
        lines = [line[:-1] for line in f]
    return lines

def get_directory(base: Path) -> Path:
    directory = Path(base).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory


def get_container(base: Path, identifier: str):
    return get_directory(Path(base, identifier))


def get_resource_identifier(base: Path, name: str, suffix: str) -> Path:
    return Path(base, name).with_suffix(suffix)


def remove_directory(base: Path) -> None:
    rmtree(base)
    
def get_command(name: str) -> bool:
    COMMAND = os.environ.get(name) or "NO"
    return COMMAND == "YES"
    
