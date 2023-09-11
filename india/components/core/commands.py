from typing import Dict
from pathlib import Path

class Commands:
    def __init__(self) -> None:
        self._table: Dict[str, str] = {}
        
    @property
    def table(self) -> Dict[str, str]:
        return self._table
    
    def write(self, commands_home: Path) -> None:
        for key, value in self.table.items():
            file_identifier = Path(commands_home, key)
            with open(file_identifier, "w") as target:
                target.write(value + "\n")
                                   
