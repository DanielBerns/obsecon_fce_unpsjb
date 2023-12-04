from collections import (Counter, defaultdict)
import datetime
import json
from pathlib import Path
from typing import (DefaultDict, 
                    Dict, 
                    Tuple)

from components.helpers import (write_json, 
                                get_directory, 
                                get_timestamp, 
                                get_resource)


class Metadata:

    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = get_resource(self.directory, 'store', '.json')
        self._events: DefaultDict[str, DefaultDict[str, Dict]] = \
            defaultdict(lambda: defaultdict(dict))
        if self.store.exists():
            self.load_events()
        else:
            self.initialize_events()
        
    @property
    def directory(self) -> Path:
        return self._directory
    
    @property
    def store(self) -> Path:
        return self._store

    @property
    def events(self) -> DefaultDict[str, DefaultDict[str, Dict]]:
        return self._events
    
    def initialize_events(self) -> None:
        self.add_item('.', 'creation', {'timestamp': get_timestamp()})
        save_json(self.store, self.events)

    def load_events(self) -> None:
        with open(self.store, 'r') as source:
            for line in source:
                event = json.loads(line)
                self.add_item(event['identifier'], 
                           event['attribute'], 
                           event['value'])

    def save_events(self) -> None:
        with open(self.store, 'w') as target:
            for identifier, attribute, value in self.items():
                event = {'identifier': identifier,
                         'attribute': attribute,
                         'value': value}
                target.write(f"{json.dumps(event):s}\n")
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        self.save_events()

    def items(self) -> Tuple[str, str, Dict]:
        for identifier, sample in self.events.items():
            for attribute, value in sample.items():
                yield identifier, attribute, value 

    def add_item(self, identifier: str, attribute: str, value: Dict) -> None:
        self.events[identifier][attribute] = value
