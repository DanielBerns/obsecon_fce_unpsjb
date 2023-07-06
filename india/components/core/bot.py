from pathlib import Path
from components.core.treestore import TreeStore


class Bot:
    def __init__(self, store: TreeStore):
        self._store = store

    @property
    def store(self) -> TreeStore:
        return self._store

    def samples(self, initial: int = 0, top: int = -1) -> Generator[Path]:
        for sample in self.store.samples(initial=initial, top=top):
            yield sample
