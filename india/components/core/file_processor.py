from pathlib import Path
from typing import Optional, TextIO
from components.core.processor import Processor

class FileProcessor(Processor):
    def __init__(self):
        super().__init__()
        self._source_identifier: Optional[Path] = None
        self._target_identifier: Optional[Path] = None
        
    @property
    def source_identifier(self) -> Optional[Path]:
        return self._source_identifier
    
    @source_identifier.setter
    def source_identifier(self, value: Optional[Path]) -> None:
        self._source_identifier = value

    @property
    def target_identifier(self) -> Optional[Path]:
        return self._target_identifier
    
    @target_identifier.setter
    def target_identifier(self, value: Optional[Path]) -> None:
        self._target_identifier = value

    def execute(self) -> None:
        with open(self.source_identifier, 'r') as source:
            self.read(source)
        with open(self.target_identifier, 'w') as target:
            self.write(target)
            
    def read(self, source: TextIO) -> None:
        pass
    
    def write(self, target: TextIO) -> None:
        pass
