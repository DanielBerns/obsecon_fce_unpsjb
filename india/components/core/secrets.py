from pathlib import Path
from typing import Dict
from os import walk

from components.helpers import get_container, get_resource, load_json, save_json

import pdb

class Secrets:
    def __init__(self, 
                 identifier: str,
                 filename: str) -> None:
        pdb.set_trace()
        self._content: Dict[str, str] = {}
        self._filename: str = filename

    @property
    def content(self) -> Dict[str, str]:
        return self._content

    @property
    def filename(self) -> str:
        return self._filename

    def read(self, home: Path) -> None:
        for root, dirs, files in walk(home):
            for key in dirs:
                container = get_container(Path(root), key)
                resource = get_resource(container, self.filename, ".json")
                try:
                    value = load_json(resource)
                except Exception:
                    value = {}
                self.content[key] = value

    def write(self, home: Path) -> None:
        for key, value in self.content.items():
            container = get_container(home, key)
            resource = get_resource(
                container, 
                self.identifier, '.json')
            save_json(resource, value)
            
