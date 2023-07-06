from typing import Protocol, Dict, List
from pathlib import Path


class TextReader(Protocol):
    def read_text(self, resource: Path) -> List:
        return []
