import os
from pathlib import Path
from typing import Generator, Tuple
from components.core.metadata import Metadata
from components.helpers import get_timestamp, get_container, classname

class SampledDataset:
    def __init__(self, home: Path):
        self._home = home
        self._metadata = Metadata(home)
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def metadata(self) -> Metadata:
        return self._metadata

    def start(self) -> None:
        print(f'{classname(self):s}.start at {str(self.home):s}')
    
    def stop(self) -> None:
        self.metadata.stop()
        print(f'{classname(self):s}.stop  at {str(self.home):s}')

    def walk(self) -> Path:
        for root, dirs, files in os.walk(self.home):
            for dd in dirs:
                yield Path(self.home, dd)

    def create_sample(self, identifier: str) -> Tuple[str, Path]:
        sample_key, sample_path = identifier, get_container(self.home, identifier)
        self.metadata.add(
            sample_key, 
            f'{classname(self):s}.create_sample.path', 
            str(sample_path))
        self.metadata.add(
            sample_key, 
            f'{classname(self):s}.create_sample.timestamp', 
            get_timestamp())        
        return sample_key, sample_path
    
    def get_sample(self, identifier: str) -> Tuple[str, Path]:
        return identifier, get_container(self.home, identifier)
    
