from logging import error
import os
from pathlib import Path
from typing import Generator, Optional

from components.core.metadata import Metadata
from components.core.sample_store import SampleStore
from components.helpers import get_timestamp, get_container, classname


class FlatStore(SampleStore):
    def __init__(self, container: Path, identifier: str) -> None:
        super().__init__(container, identifier)
        self._metadata = Metadata(get_container(self.home, "metadata"))
        self.metadata.start()

    @property
    def metadata(self) -> Metadata:
        return self._metadata

    def stop(self) -> None:
        self.metadata.stop()
        
    def walk_the_samples(self) -> Path:
        for root, dirs, files in os.walk(self.home):
            for dd in dirs:
                yield Path(self.home, dd)

    def create_sample(
        self, 
        key: Optional[str] = None, 
        number: int = -1
        ) -> Path:
        identifier = key if key else get_timestamp()
        sample = get_container(self.home, identifier)
        self.metadata.add("samples", identifier, str(self.index.value))
        return sample

    def get_sample(
        self, 
        key: Optional[str] = None, 
        number: int = -1
        ) -> Path:
        if key is None:
            error(f"{classname(self):s}.get_sample: 1")
            raise SampleStoreError(
                f"{classname(self):s}.get_sample: key is None"
                )
        sample = Path(self.home, key)
        if sample.exists():
            pass
        else:
            error(f"{classname(self):s}.get_sample: 2")            
            raise SampleStoreError(
                f"{classname(self):s}.get_sample: invalid key {key:s}"
                )
        return sample
    
    def samples(self) -> Generator[Path, None, None]:
        all_the_samples = self.metadata.events["samples"]
        for identifier, index in all_the_samples.items():
            yield self.get_sample(identifier)
