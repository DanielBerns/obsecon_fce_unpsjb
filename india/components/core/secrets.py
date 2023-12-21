from pathlib import Path
from typing import Dict
from os import walk

from components.helpers import get_container, get_resource, load_json, save_json

import pdb

class Secrets:

    @staticmethod
    def read(container: Path, 
             filename: str = "secrets"
             ) -> Dict[str, str]:
        pdb.set_trace()
        resource: Path = get_resource(container, filename, '.json')
        try:
            value: Dict = load_json(resource)
        except Exception:
            value: Dict = {}
        content: Dict[str, str] = {str(k):str(v) for k, v in value.items()}
        return content

    @staticmethod
    def write(container: Path, 
              content: Dict[str, str],
              filename: str = "secrets"
              ) -> None:
        resource = get_resource(container, filename, '.json')
        save_json(resource, content)
