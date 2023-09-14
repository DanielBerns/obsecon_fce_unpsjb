from collections import defaultdict, Counter
import datetime
import json
from pathlib import Path
from typing import Dict, Tuple, DefaultDict, Generator

from components.helpers import (
    save_json,
    get_directory,
    get_timestamp,
    get_resource,
)


class Metadata:
    chrF = chr(15)

    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._resource: Path = get_resource(
            self.directory, "store", ".json"
        )
        self._events: DefaultDict[str, DefaultDict[str, str]] = defaultdict(
            lambda: defaultdict(str)
        )
        if self.resource.exists():
            self.load_events()
        else:
            self.initialize_events()

    @property
    def directory(self) -> Path:
        return self._directory

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def events(self) -> DefaultDict[str, DefaultDict[str, Dict]]:
        return self._events

    def initialize_events(self) -> None:
        first_event = self.events[get_timestamp()]
        self.save_events()

    def load_events(self) -> None:
        with open(self.resource, "r") as source:
            for number, line in enumerate(source):
                try:
                    parts = line.split(chrF)
                    name, value_json = parts[0], parts[1]
                    value = json.loads(value_json)
                    event = self.events[name]
                    for k, v in value.items():
                        event[k] = v
                except IndexError:
                    logging.warning("components.core.Metadata.load_events")
                    logging.warning(f"  error at {str(self.store):s} #{number:d}")  
                    logging.warning(f"  {line:s}")
                except AttributeError:
                    logging.warning("components.core.Metadata.load_events")
                    logging.warning(f"  error at {str(self.store):s} #{number:d}")  
                    logging.warning(f"  {value_json}")                    

    def save_events(self) -> None:
        with open(self.resource, "w") as target:
            for identifier, value in self.events.items():
                target.write(
                    f"{identifier:s}{Metadata.chrF:s}{json.dumps(value):s}\n")

    def start(self) -> None:
        pass

    def stop(self) -> None:
        self.save_events()

    def items(self) -> Generator[Tuple[str, str, str], None, None]:
        for identifier, sample in self.events.items():
            for attribute, value in sample.items():
                yield identifier, attribute, value

    def add(self, 
            identifier: str, 
            attribute: str, 
            value: str) -> None:
        self.events[identifier][attribute] = value
