import os
from pathlib import Path
from typing import Generator, Tuple
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

    def start(self) -> None:
        print(f'SampledDataset.start at {str(self.home):s}')
    
    def stop(self) -> None:
        self.metadata.stop()
        print(f'SampledDataset.stop  at {str(self.home):s}')

    def walk(self) -> Path:
        for root, dirs, files in os.walk(self.home):
            for dd in dirs:
                yield Path(self.home, dd)
 
    def create_sample(self) -> Tuple[str, Path]:
        timestamp = get_timestamp()
        sample_path = get_container(self.home, timestamp)
        self.metadata.add(timestamp, 'created', str(sample_path))
        return timestamp, sample_path
