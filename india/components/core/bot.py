from pathlib import Path
from components.core.treestore import SampleTaskFactory, TreeStore


class Bot:
    def __init__(self, store: TreeStore):
        self._store = store

    @property
    def store(self) -> TreeStore:
        return self._store

    def process(self, 
                pipeline: SampleTaskFactory, 
                reset_next_to_process: bool = True) -> None:
        processor = TreeStoreProcessor(
            self.store,
            pipeline,
            reset_next_to_process)
        processor.execute()

    def create(self, 
               pipeline: SampleTaskFactory) -> None:
        processor = TreeStoreProcessor(
            self.store,
            pipeline,
            reset_next_to_process)
        processor.create()        
        
