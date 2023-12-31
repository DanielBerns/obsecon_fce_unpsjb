from logging import info, debug, error
from pathlib import Path
from typing import Generator, Tuple, Dict, Protocol
import json

from components.core.metadata import Metadata
from components.helpers import get_container, get_resource, classname


class SampleStoreError(Exception):
    pass


class Index:
    def __init__(self, resource: Path) -> None:
        self._resource: Path = resource
        if self.resource.exists():
            # restarting Index
            value = self.read()
            self._value = int(value["index"])
        else:
            # initialize Index
            self._value = 0
            self.write()

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, update: int) -> None:
        self._value = update
        self.write()

    def write(self) -> None:
        value = {"index": str(self.value)}
        with open(self.resource, "w") as target:
            json.dump(value, target)

    def read(self) -> Dict[str, str]:
        with open(self.resource, "r") as source:
            values = json.load(source)
        return values


class SampleStore:
    def __init__(self, container: Path, identifier: str) -> None:
        self._home = get_container(container, identifier)
        self._base = get_container(self.home, "base")
        resource = get_resource(self.home, "index", ".json")
        self._index = Index(resource)

    @property
    def home(self) -> Path:
        return self._home

    @property
    def base(self) -> Path:
        return self._base

    @property
    def index(self) -> Index:
        return self._index

    def start(self) -> None:
        info(f"{classname(self):s}.start() with index {self.index.value:d}")

    def stop(self) -> None:
        self.index.write()
        info(f"{classname(self):s}.stop() with index {self.index.value:d}")

    def get_key(self) -> str:
        raise SampleStoreError(f"{classname(self):s}.get_key() not implemented")

    def create_sample(self) -> Path:
        key = self.get_key()
        sample = Path(self.home, key)
        sample.mkdir(mode=0o700, parents=True, exist_ok=False)
        return sample

    def get_sample(self, key: str = "", number: int = -1) -> Path:
        sample = Path(self.home, key)
        return sample


class SampleTask:
    def __init__(self, identifier: str):
        self._identifier = identifier
        self._iteration = 0

    @property
    def identifier(self) -> str:
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
        super().__init__("EmptySampleTask")

    def start(self, target: Path) -> None:
        super().start(target)

    def execute(self, sample: Path) -> None:
        super().execute(sample)

    def stop(self, target: Path) -> None:
        super().stop(target)


class SampleTaskFactory(Protocol):
    def execute(self) -> Generator[SampleTask, None, None]:
        pass


class NextToProcessMetadata(Metadata):
    def __init__(self, base: Path):
        super().__init__(base)

    @property
    def next_to_process(self) -> int:
        value = self.events["next_to_process"]["value"]
        return int(value)

    @next_to_process.setter
    def next_to_process(self, value: int) -> None:
        self.add("next_to_process", "value", str(value))
        self.save_events()


class Pipeline:
    def __init__(self) -> None:
        self._tasks: Dict[str, SampleTask] = {}

    def add(self, task: SampleTask) -> None:
        self._tasks[task.identifier] = task

    def tasks(self) -> Generator[SampleTask, None, None]:
        for identifier, task in self._tasks.items():
            yield task

    def remove(self, identifier: str) -> None:
        try:
            del self._tasks[identifier]
        except KeyError:
            pass


# class PipelineDriver:
#
#     @staticmethod
#     def sample_per_task(pipeline: Pipeline, store: TreeStore) -> None:
#         for sample in store.samples():
#             for task in pipeline.tasks():
#                 task.execute(sample)
#
#     @staticmethod
#     def task_per_sample(store: TreeStore, pipeline: Pipeline) -> None:
#         for task in pipeline.tasks():
#             for sample in store.samples():
#                 task.execute(sample)
