from pathlib import Path
from typing import Optional
from components.core.processor import Processor

class FileProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()
        self._origin_identifier: Optional[Path] = None
        self._target_identifier: Optional[Path] = None        

    @property
    def origin_identifier(self) -> Optional[Path]:
        return self._origin_identifier
    
    @origin_identifier.setter
    def origin_identifier(self, value: Path) -> None:
        self._origin_identifier = value
        
    @property
    def target_identifier(self) -> Optional[Path]:
        return self._target_identifier
    
    @target_identifier.setter
    def target_identifier(self, value: Path) -> None:
        self._target_identifier = value
        
    def execute(self) -> None:
        self.read()
        self.process()
        self.write()
            
    def read(self) -> None:
        pass

    def process(self) -> None:
        pass
    
    def write(self) -> None:
        pass

