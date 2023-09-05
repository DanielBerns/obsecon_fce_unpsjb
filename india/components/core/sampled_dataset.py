import os
from pathlib import Path
from typing import Generator
from components.core.metadata import Metadata

class SampledDataset:
    def __init__(self, home: Path):
        self._home = home
        self._metadata = Metadata(directory)
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def metadata(self) -> Metadata:
        return self._metadata

    def sample_container(self, identifier: str) -> Path:
        container = get_container(self.home, sample)
    
    def start(self) -> None:
        print('SampledDataset.start')
    
    def stop(self) -> None:
        print('SampledDataset.stop')

    def samples(self) -> Path:
        for root, dirs, files in os.walk(self.home):
            for dd in dirs:
                yield Path(self.home, dd)
 
 
@contextmanager
def create_sampled_dataset(home: Path) -> Generator[SampledDataset, None, None]:
    resource = SampledDataset(home)
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(str(message))
    finally:
        resource.stop()
 
