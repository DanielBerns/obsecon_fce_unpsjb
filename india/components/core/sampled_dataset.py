import os
from pathlib import Path
from typing import Generator
from components.core.metadata import Metadata
from components.helpers import get_timestamp, get_container

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

    def sample_container(self, identifier: str) -> Path:
        container = get_container(self.home, sample)
    
    def start(self) -> None:
        print(f'SampledDataset.start at {str(self.home):s}')
    
    def stop(self) -> None:
        self.metadata.stop()
        print(f'SampledDataset.stop  at {str(self.home):s}')

    def walk(self) -> Path:
        for root, dirs, files in os.walk(self.home):
            for dd in dirs:
                yield Path(self.home, dd)
 
    def create_sample_path(self) -> Path:
        timestamp = get_timestamp()
        sample = get_container(self.home, timestamp)
        self.metadata.add_item('samples',timestamp, {'path': str(sample)})
        return sample
        
    
