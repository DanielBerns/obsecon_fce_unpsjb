from pathlib import Path
from components.core.treestore import TreeStore

class Bot:
    def __init__(self, store: TreeStore):
        self._store = store
        
    @property
    def store(self) -> TreeStore:
        return self._store
    
    def get_samples(self, top: int = -1) -> Path:
        for sample in self.store.samples:
            yield sample
 
