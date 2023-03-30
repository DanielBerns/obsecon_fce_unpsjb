from collections import defaultdict, Counter
import datetime
import json
from pathlib import Path
from typing import Dict, Tuple, DefaultDict

from components.helpers import save_json, get_directory, get_timestamp


class Metadata:

    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = Path(self.directory, 'store').with_suffix('.json')
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
                self.add_item(event['first_key'], 
                           event['second_key'], 
                           event['value'])

    def save_events(self) -> None:
        with open(self.store, 'w') as target:
            for first_key, second_key, value in self.items():
                event = {'first_key': first_key,
                         'second_key': second_key,
                         'value': value}
                target.write(f"{json.dumps(event):s}\n")
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        self.save_events()

    def items(self) -> Tuple[str, str, Dict]:
        for first_key, sample in self.events.items():
            for second_key, value in sample.items():
                yield first_key, second_key, value 

    def add_item(self, first_key: str, second_key: str, value: Dict) -> None:
        self.events[first_key][second_key] = value
