import json
from pathlib import Path
from shutil import rmtree
import logging
from typing import Tuple, Generator, Protocol, List, Optional
from contextlib import contextmanager

from components.core.metadata import Metadata
from components.core.sample_store import (SampleStore, 
                                          Pipeline, 
                                          PipelineDriver, 
                                          NextToProcessMetadata)
from components.helpers import (get_container, 
                                get_resource, 
                                get_timestamp, 
                                classname)


class TreeStoreError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

import pdb

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


class TreeStore(SampleStore):
    def __init__(self, container: Path, identifier: str) -> None:
        super().__init__(container, identifier)

    def create_sample(self) -> Path:
        pdb.set_trace()
        first_digit, second_digit, third_digit = base_256(self.index.value)
        self.index.value += 1
        sample = Path(
            self.base,
            f"{first_digit:>03d}",
            f"{second_digit:>03d}",
            f"{third_digit:>03d}",
        )
        sample.mkdir(mode=0o700, parents=True, exist_ok=False)
        return sample

    def get_sample(self, key: Optional[str] = None, number: int = -1) -> Path:
        if 0 <= number < self.index.value:
            first_digit, second_digit, third_digit = base_256(number)
            sample = Path(
                self.base,
                f"{first_digit:>03d}",
                f"{second_digit:>03d}",
                f"{third_digit:>03d}",
            )
            return sample
        else:
            raise TreeStoreError(
                f"{classname(self):s}.get_sample: {number:d} out of range [0,{self.index.value:d})"
                )
                                                                         
    def samples(self) -> Generator[Path, None, None]:
        for k in range(0, self.index.value):
            first_digit, second_digit, third_digit = base_256(k)
            sample = Path(
                self.tree,
                f"{first_digit:>03d}",
                f"{second_digit:>03d}",
                f"{third_digit:>03d}",
            )
            yield sample




class TreeStoreDriver:
    def __init__(self, store: TreeStore) -> None:
        self._store = store
        self._metadata = NextToProcessMetadata(store.base)
        self._pipeline = Pipeline()

    @property
    def store(self) -> TreeStore:
        return self._store

    @property
    def metadata(self) -> NextToProcessMetadata:
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

    def create_sample(self) -> None:
        sample = self.store.new_sample()        
        for sample_task in self.pipeline.execute():
            sample_task.execute(sample)
    
    def process_samples(self, reset_next_to_process: bool) -> None:
        if reset_next_to_process:
            self.metadata.next_to_process = 0
        next_to_process = self.metadata.next_to_process
        self.metadata.next_to_process = self.store.index
        logging.info(f"{classname(self):s}.process_samples: start")        
        for sample_task in self.pipeline.execute():
            sample_task.start(self.store.base)
        logging.info(f"{classname(self):s}.process_samples: execute")        
        for sample in self.store.samples(first=next_to_process):
            for sample_task in self.pipeline.execute():
                try:
                    sample_task.execute(sample)
                except Exception as message:
                    logging.error(f"{classname(self):s}.process_samples: error")
                    logging.error(f"  {str(sample):s}")                    
                    logging.error(f"  {str(message):s}")
        logging.info(f"{classname(self):s}.process_samples: stop")                        
        for sample_task in self.pipeline.execute():
            sample_task.stop(self.store.base)


@contextmanager
def create_treestore_driver(treestore_home: Path, identifier: str) -> None:
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

