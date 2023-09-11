from pathlib import Path
from components.core.treestore import (SampleTaskFactory, 
                                       TreeStore, 
                                       TreeStoreDriver)

class Bot:
    def __init__(self, store: TreeStore) -> None:
        self._store = store
        self._driver = TreeStoreDriver(store)

    @property
    def driver(self) -> TreeStoreDriver:
        return self._driver

    def create(self) -> None:
        self.driver.create()

    def process(self, reset_next_to_process: bool = True) -> None:
        self.driver.process(reset_next_to_process)

        
