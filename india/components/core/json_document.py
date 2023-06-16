import json
from pathlib import Path
from typing import Dict, Protocol

from components.helpers import get_directory, get_resource_identifier


class JSONSource(Protocol):
    def events(self) -> Dict:
        yield from ()


class JSONDocument:

    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = get_resource_identifier(self.directory, 'store', '.json')        
        
    @property
    def directory(self) -> Path:
        return self._directory
    
    @property
    def store(self) -> Path:
        return self._store

    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass

    def events(self) -> Dict:
        with open(self.store,'r') as source:
            for line in source:
                event = json.loads(line)
                yield event
    
    def update(self, source: JSONSource) -> None:
        with open(self.store,'a') as target:
            for event in source.events():
                line = json.dumps(event)
                target.write(f"{line:s}\n")
