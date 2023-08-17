from pathlib import Path
from components.core.treestore import TreeStore


class Bot:
    def __init__(self, store: TreeStore):
        self._store = store

    @property
    def store(self) -> TreeStore:
        return self._store
