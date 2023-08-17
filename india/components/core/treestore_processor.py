from typing import Protocol, Tuple, Optional
from pathlib import Path

from components.core import TreeStore, Metadata
from components.helpers import get_container, get_timestamp


class SampleTask(Protocol):
    def execute(self, sample: Path) -> None:
        pass

    def report(self, target: Path) -> None:
        pass

class EmptySampleTask:
    def __init__(self):
        pass
    
    def execute(self, sample: Path) -> None:
        pass

    def report(self, target: Path) -> None:
        pass


SAMPLE_TASK_EMPTY_PIPELINE = [EmptySampleTask()]


class SampleTaskFactory(Protocol):
    def execute(self) -> SampleTask:
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


class TreeStoreProcessorException(Exception):
    def __init__(self, message: str = "Error"):
        super().__init__("TreeStoreProcessor: " + message)


class TreeStoreProcessor:
    def __init__(self, 
                 store: TreeStore,
                 pipeline: Optional[List[SampleTask]] = None) -> None:
        self._store = store
        self._metadata = TreeStoreProcessorMetadata(store.base)
        self._pipeline = pipeline if pipeline else SAMPLE_TASK_EMPTY_PIPELINE

    @property
    def store(self) -> TreeStore:
        return self._store

    @property
    def metadata(self) -> TreeStoreProcessorMetadata:
        return self._metadata

    @property
    def pipeline(self) -> List[SampleTask]:
        return self._pipeline
    
    @pipeline.setter
    def pipeline(self, value: List[SampleTask]) -> None:
        if value:
            self._pipeline = value
        else:
            raise TreeStoreProcessorException("zero length SampleTask pipeline")

    def execute(self) -> None:
        next_to_process = self.metadata.next_to_process
        self.metadata.next_to_process = self.store.index
        for sample in self.store.samples(first=next_to_process):
            for sample_task in self.pipeline:
                sample_task.execute(sample)
        target = get_container(store.base, 'target', get_timestamp())
        for sample_task in self.pipeline:
            sample_task.report(target)

