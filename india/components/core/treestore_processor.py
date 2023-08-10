from typing import Protocol, Tuple, Optional
from pathlib import Path

from components.core import TreeStore, Metadata


class SampleTask(Protocol):
    def execute(self, sample: Path) -> None:
        pass


class EmptySampleTask:
    def __init__(self):
        pass
    
    def execute(self, sample: Path) -> None:
        pass


class TreeStoreProcessorMetadata(Metadata):
    def __init__(self, base: Path):
        super().__init__(base)

    @property
    def next_to_process(self) -> Tuple[int, int]:
        processed_samples = self.events["samples"]["processed"]
        return processed_samples.get("next_to_process", 0)

    @next_to_process.setter
    def next_to_process(self, value: int) -> None:
        self.events["samples"]["processed"]["next_to_process"] = value
        self.save_events()


class TreeStoreProcessor:
    def __init__(self, 
                 store: TreeStore,
                 sample_task: Optional[SampleTask] = None) -> None:
        self._store = store
        self._metadata = TreeStoreProcessorMetadata(store.base)
        self._sample_task = sample_task if sample_task else EmptySampleTask()

    @property
    def store(self) -> TreeStore:
        return self._store

    @property
    def metadata(self) -> TreeStoreProcessorMetadata:
        return self._metadata

    @property
    def sample_task(self) -> SampleTask:
        return self._sample_task
    
    @sample_task.setter
    def sample_task(self, value: SampleTask) -> None:
        self._sample_task = value

    def execute(self) -> None:
        next_to_process = self.metadata.next_to_process
        self.metadata.next_to_process = self.store.index
        for sample in self.store.samples(first=next_to_process):
            self.sample_task.execute(sample)
