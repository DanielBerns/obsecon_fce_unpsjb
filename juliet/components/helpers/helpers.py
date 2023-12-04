from collections import defaultdict, Counter
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Generator
from shutil import rmtree


indentation = "    "


def classname(thing: Any) -> str:
    return thing.__class__.__name__


def i(n: int) -> str:
    return indentation * n


def aware_utcnow(offset: timedelta):
    return datetime.now(timezone(offset))



# print(aware_utcnow())
# print(aware_utcfromtimestamp(0))
# print(naive_utcnow())
# print(naive_utcfromtimestamp(0))

CDR = -timedelta(hours=3)

def get_timestamp(separator: str = "", offset: timedelta = CDR) -> str:
    now = aware_utcnow(offset)
    timestamp = separator.join(
        [
            f"{now.year:4d}{now.month:02d}",
            f"{now.day:02d}{now.hour:02d}",
            f"{now.minute:02d}",
            f"{now.second:02d}",
        ]
    )
    return timestamp

def read_json(data_json: Path) -> Dict[str, str]:
    data = None
    with open(data_json, "r") as origin:
        data = json.load(origin)
    return data

def write_json(data_json: Path, data: Dict) -> None:
    with open(data_json, "w") as target:
        json.dump(data, target)

def read_text(origin: Path) -> str:
    # get text from utf-8 encoded file
    with open(origin, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def write_text(target: Path, text: str) -> None:
    with open(target, 'w', encoding="utf-8") as f:
        f.write(text)

def read_text_lines(origin: Path) -> Generator[str, None, None]:
    with open(origin, 'r', encoding='utf-8') as f:
        yield from (line[:-1] for line in f)

def write_text_lines(target: Path) -> Generator[int, str, None]:
    number = 0
    with open(target, 'w', encoding="utf-8") as f:
        text_line = yield number
        if text_line:
            number += 1
            target.write(text_line + '\n')

def get_directory(base: Path) -> Path:
    directory = Path(base).expanduser()
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    return directory

def get_home(root: str,
             project: str,
             version: str,
             mode: str,
             application: str,
             ) -> Path:
    return get_directory(
        Path(root, project, version, mode, application)
        )

def get_container(base: Path, identifier: str):
    return get_directory(Path(base, identifier))

def get_resource(
    base: Path, 
    name: str, 
    suffix: str
    ) -> Path:
    return get_directory(Path(base, name)).with_suffix(suffix)

def get_resource_with_timestamp(
    base: Path, 
    name: str,
    suffix: str) -> Path:
    
    timestamp = get_timestamp()
    resource = get_resource(
        base, f"{name:s}_{timestamp:s}", suffix
        )
    return resource


def remove_directory(base: Path) -> None:
    rmtree(base)

    
def get_environment_variable(name: str, default_value: str = "-") -> bool:
    return os.environ.get(name) or default_value
