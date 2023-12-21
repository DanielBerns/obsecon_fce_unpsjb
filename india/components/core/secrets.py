from pathlib import Path
from typing import Dict
from os import walk

from components.helpers import get_container, get_resource, load_json, save_json

import pdb

class Secrets:

    @staticmethod
    def read(base: Path, 
             filename: str = "secrets"
             ) -> Dict[str, Dict[str, str]]:
        content: Dict[str, Dict[str, str]] = {}
        for _base, dirs, files in walk(base):
            for key in dirs:
                container = get_container(Path(_base), key)
                resource = get_resource(container, filename, ".json")
                try:
                    value = load_json(resource)
                except Exception:
                    value = {}
                content[key] = {str(k):str(v) for k, v in value.items()}

    @staticmethod
    def write(base: Path, 
              content: Dict[str, Dict[str, str]],
              filename: str = "secrets"
              ) -> None:
        for key, value in content.items():
            container = get_container(base, key)
            resource = get_resource(container, filename, '.json')
            save_json(resource, value)
