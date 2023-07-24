from pathlib import Path
from typing import Optional
from components.core.processor import Processor

class FileProcessor(Processor):
    def __init__(self):
        super().__init__()
        self._file_identifier: Optional[Path] = None
        
    @property
    def file_identifier(self) -> Optional[Path]:
        return self._file_identifier
    
    @file_identifier.setter
    def file_identifier(self, value: Optional[Path]) -> None:
        self._file_identifier = value
