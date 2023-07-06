from pathlib import Path
from components.core.treestore import TreeStore


class Bot:
    def __init__(self, store: TreeStore):
        self._store = store

    @property
    def store(self) -> TreeStore:
        return self._store

    # def samples(self, first: int = 0, top: int = -1) -> Generator[Path, None, None]:
    #     for sample in self.store.samples(first=first, top=top):
    #         yield sample
