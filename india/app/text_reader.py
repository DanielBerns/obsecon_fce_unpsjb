from typing import Protocol, Dict, List

class TextReader(Protocol):
    def read_text(self, resource: Path) -> List:
        return []
