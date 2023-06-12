from components.core import TreeStore 

class SampleProcessor(Protocol):
    def execute(self, sample: Path) -> None:
        pass
    
class TreeStoreProcessor:
    def __init__(self, store: TreeStore) -> None:    
        self._store = store

    @property
    def store(self) -> TreeStore:
        return self._store
    
    def execute(self, sample_processor: SampleProcessor):
        for sample in self.store.samples():
            sample_processor.execute(sample)    
