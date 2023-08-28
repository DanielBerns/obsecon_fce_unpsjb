from collections import defaultdict, Counter
import datetime
import json
from pathlib import Path
from typing import Dict, Tuple, DefaultDict, Generator

from components.helpers import (
    save_json,
    get_directory,
    get_timestamp,
    get_resource_identifier,
)


class Metadata:
    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._resource: Path = get_resource_identifier(
            self.directory, "metadata", ".json"
        )
        self._events: DefaultDict[str, DefaultDict[str, Dict]] = defaultdict(
            lambda: defaultdict(dict)
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
        self.add_item(".", "creation", {"timestamp": get_timestamp()})
        save_json(self.resource, self.events)

    def load_events(self) -> None:
        with open(self.resource, "r") as source:
            for line in source:
                event = json.loads(line)
                print(str(event))
                try:
                    self.add_item(
                        event["identifier"], event["attribute"], event["value"]
                    )
                except KeyError:
                    for key, value in event.items():
                        print(key, str(value))

    def save_events(self) -> None:
        with open(self.resource, "w") as target:
            for identifier, attribute, value in self.items():
                event = {
                    "identifier": identifier,
                    "attribute": attribute,
                    "value": value,
                }
                target.write(f"{json.dumps(event):s}\n")

    def start(self) -> None:
        pass

    def stop(self) -> None:
        self.save_events()

    def items(self) -> Generator[Tuple[str, str, Dict], None, None]:
        for identifier, sample in self.events.items():
            for attribute, value in sample.items():
                yield identifier, attribute, value

    def add_item(self, 
                 identifier: str, 
                 attribute: str, 
                 value: Dict[str, str]) -> None:
        self.events[identifier][attribute] = value
