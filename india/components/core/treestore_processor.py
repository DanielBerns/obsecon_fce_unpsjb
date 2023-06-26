from typing import Protocol, Tuple
from pathlib import Path 

from components.core import TreeStore, Metadata

class SampleProcessor(Protocol):
    def execute(self, sample: Path) -> None:
        pass
    

class TreeStoreProcessorMetadata(Metadata):
    def __init__(self, base: Path):
        super().__init__(base)
    
    @property
    def next_to_process(self) -> Tuple[int, int]:
        processed_samples = self.events['samples']['processed']
        return processed_samples.get('next_to_process', 0)
    
    @next_to_process.setter
    def next_to_process(self, value: int) -> None:
        self.events['samples']['processed']['next_to_process'] = value
        self.save_events()
        

class TreeStoreProcessor:
    def __init__(self, 
                 store: TreeStore
                 ) -> None:    
        self._store = store
        self._metadata = TreeStoreProcessorMetadata(store.base)

    @property
    def store(self) -> TreeStore:
        return self._store
    
    @property
    def metadata(self) -> TreeStoreProcessorMetadata:
        return self._metadata
    
    def execute(self, 
                sample_processor: SampleProcessor
                ) -> None:
        for sample in self.store.samples(self.metadata.next_to_process):
            sample_processor.execute(sample)
        self.store.write()
            
    
