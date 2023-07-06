import json
from pathlib import Path
from shutil import rmtree
import logging
from typing import Tuple

from components.helpers import get_container


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

    def samples(self, first: int = 0, top: int = -1) -> Generator[Path]:
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
