import json
from pathlib import Path
from shutil import rmtree
import logging
from typing import Tuple, Generator, Protocol, List, Optional
from contextlib import contextmanager

from components.core.metadata import Metadata
from components.helpers import get_container, get_timestamp


class TreeStoreError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def base_256(number: int) -> Tuple[int, int, int]:
    assert 0 <= number < 16777216
    third_digit = number % 256
    number >>= 8
    second_digit = number % 256
    first_digit = number >> 8
    return first_digit, second_digit, third_digit


def base_10(first_digit: int, second_digit: int, third_digit: int) -> int:
    return (((first_digit << 8) + second_digit) << 8) + third_digit


def erase_directory(base: Path) -> None:
    rmtree(base, ignore_errors=True)


class TreeStore:
    def __init__(self, home: Path, identifier: str) -> None:
        """
        home: path where TreeStore lives
        identifier: the name of the TreeStore
        """
        base = get_container(home, identifier)
        index_resource = Path(base, "index").with_suffix(".json")
        self._base = base
        self._tree = Path(base, "tree")
        self._index_resource = index_resource
        self._index = 0
        if self.index_resource.exists():
            # restarting treestore
            values = self.read()
            self._index = values["index"]
        else:
            # creating treestore
            self.write()

    @property
    def base(self) -> Path:
        return self._base

    @property
    def tree(self) -> Path:
        return self._tree

    @property
    def index_resource(self) -> Path:
        return self._index_resource

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int) -> None:
        self._index = value
        self.write()

    def write(self) -> None:
        values = {"index": self.index}
        with open(self.index_resource, "w") as target:
            json.dump(values, target)

    def read(self) -> dict:
        with open(self.index_resource, "r") as source:
            values = json.load(source)
        return values

    def new_sample(self) -> Path:
        first_digit, second_digit, third_digit = base_256(self.index)
        self.index += 1
        sample = Path(
            self.tree,
            f"{first_digit:>03d}",
            f"{second_digit:>03d}",
            f"{third_digit:>03d}",
        )
        sample.mkdir(mode=0o700, parents=True, exist_ok=False)
        return sample

    def start(self):
        logging.info(f"treestore.start() with index {self.index:d}")

    def stop(self):
        self.write()

    def samples(self, first: int = 0, top: int = -1) -> Generator[Path, None, None]:
        if first < 0:
            raise TreeStoreError(
                f"TreeStore.samples: first {first:d} out of range (0, {self.index:d})"
            )
        elif self.index < first:
            raise TreeStoreError(
                f"TreeStore.samples: first {first:d} out of range (0, {self.index:d})"
            )
        if top == -1:
            top = self.index
        elif 0 <= top <= self.index:
            pass
        else:
            raise TreeStoreError(
                f"TreeStore.samples: top {top:d} out of range (0, {self.index:d})"
            )
        if first <= top:
            pass
        else:
            raise TreeStoreError(f"TreeStore.samples: top {top:d} < first {first:d}")
        for k in range(first, top):
            first_digit, second_digit, third_digit = base_256(k)
            sample = Path(
                self.tree,
                f"{first_digit:>03d}",
                f"{second_digit:>03d}",
                f"{third_digit:>03d}",
            )
            yield sample



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
    
    def start(self, target: Path) -> None:
        print(f"start {self.identifier:<20s} - total iteration: {self.iteration:d}")
        
    def execute(self, sample: Path) -> None:
        self.iteration += 1
        print(f"{self.identifier:<20s} - {str(sample):s}: {self.iteration:d}")

    def stop(self, target: Path) -> None:
        print(f"stop {self.identifier:<20s} - total iteration: {self.iteration:d}")
        

class EmptySampleTask(SampleTask):
    def __init__(self):
        super().__init__('EmptySampleTask')

    def start(self, target: Path) -> None:
        super().start(target)
    
    def execute(self, sample: Path) -> None:
        super().execute(sample)

    def stop(self, target: Path) -> None:
        super().stop(target)



class SampleTaskFactory(Protocol):
    def execute(self) -> Generator[SampleTask, None, None]:
        pass


class TreeStoreMetadata(Metadata):
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

class Pipeline:
    def __init__(self) -> None:
        self._tasks: List[SampleTask] = []

    def append(self, task: SampleTask) -> None:
        self._tasks.append(task)
        
    def execute(self) -> Generator[SampleTask, None, None]:
        for task in self._tasks:
            yield task


class TreeStoreDriver:
    def __init__(self, 
                 store: TreeStore
                 ) -> None:
        self._store = store
        self._metadata = TreeStoreMetadata(store.base)
        self._pipeline = Pipeline()

    @property
    def store(self) -> TreeStore:
        return self._store

    @property
    def metadata(self) -> TreeStoreMetadata:
        return self._metadata

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline
    
    @pipeline.setter
    def pipeline(self, value: Pipeline) -> None:
        self._pipeline = value

    @property
    def get_target_container(self):
        return get_container(self.store.base, 'target')

    def create(self) -> None:
        sample = self.store.new_sample()        
        for sample_task in self.pipeline.execute():
            sample_task.execute(sample)
    
    def process(self, reset_next_to_process: bool) -> None:
        if reset_next_to_process:
            self.metadata.next_to_process = 0
        next_to_process = self.metadata.next_to_process
        self.metadata.next_to_process = self.store.index
        for sample_task in self.pipeline.execute():
            sample_task.start(self.store.base)
        for sample in self.store.samples(first=next_to_process):
            for sample_task in self.pipeline.execute():
                sample_task.execute(sample)
        for sample_task in self.pipeline.execute():
            sample_task.stop(self.store.base)


@contextmanager
def create_treestore_driver(
    treestore_home: Path, 
    identifier: str) -> None:
    logging.info(f"start run: {str(treestore_home):s}")
    logging.info(f"  identifier: {identifier:s}")
    store = TreeStore(treestore_home, identifier)
    store.start()
    driver = TreeStoreDriver(store)
    try:
        yield driver
    except Exception as message:
        print(str(message))
    store.stop()
    logging.info(f"  done: {identifier:s}")
    logging.info(f"done run: {str(treestore_home):s}")
