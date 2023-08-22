from typing import Protocol, Tuple, List, Optional
from pathlib import Path

import pdb

from components.core import TreeStore, Metadata
from components.helpers import get_container, get_timestamp

class SampleTask:
    def __init__(self, identifier: str):
        self._identifier = identifier
        self._iteration = 0

    @property
    def identifier(self) -> int:
        return self._identifier
        
    @property
    def iteration(self) -> int:
        return self._iteration
    
    @iteration.setter
    def iteration(self, value: int) -> None:
        self._iteration = value
    
    def execute(self, sample: Path) -> None:
        self.iteration += 1
        print(f"{self.identifier:<20s} - {str(sample):s}: {self.iteration:d}")

    def report(self, target: Path) -> None:
        print(f"{self.identifier:<20s} - total iteration: {self.iteration:d}")
        

class EmptySampleTask(SampleTask):
    def __init__(self):
        super().__init__('EmptySampleTask')
    
    def execute(self, sample: Path) -> None:
        super().execute(sample)

    def report(self, target: Path) -> None:
        super().report(target)


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
                 pipeline: Optional[List[SampleTask]] = None,
                 reset_next_to_process: bool = True) -> None:
        self._store = store
        self._metadata = TreeStoreProcessorMetadata(store.base)
        self._pipeline = pipeline if pipeline else SAMPLE_TASK_EMPTY_PIPELINE
        self._reset_next_to_process = reset_next_to_process

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

    @property
    def reset_next_to_process(self) -> bool:
        return self._reset_next_to_process

    def execute(self) -> None:
        if self.reset_next_to_process:
            self.metadata.next_to_process = 997
        next_to_process = self.metadata.next_to_process
        self.metadata.next_to_process = self.store.index
        pdb.set_trace()        
        for sample in self.store.samples(first=next_to_process):
            for sample_task in self.pipeline:
                sample_task.execute(sample)
        target = get_container(Path(self.store.base, 'target'), get_timestamp())
        print(f"target {str(target):s}")
        for sample_task in self.pipeline:
            sample_task.report(target)

