from collections import defaultdict, Counter
from pathlib import Path
from typing import (
    List,
    Dict,
    Protocol,
    Union,
    Optional,
    Tuple,
    DefaultDict,
    Any,
    Generator,
)

from components.helpers import get_directory, get_resource

from components.core.events_document import EventsSource


class RowsDocument:
    function = lambda v: str(int(v * 100)) if isinstance(v, float) else str(v).lower()

    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = get_resource(self.directory, "store", ".csv")

    @property
    def directory(self) -> Path:
        return self._directory

    @property
    def store(self) -> Path:
        return self._store

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def rows(self) -> Generator[str, None, None]:
        with open(self.store, "r", encoding="utf-8") as source:
            header = source.readline()
            yield header
            for line in source:
                yield line

    def write(self, source: EventsSource) -> None:
        keys = source.events_stats.keys()
        header = "|".join(str(k) for k in keys)
        with open(self.store, "w", encoding="utf-8") as target:
            target.write(header + "\n")
            for event in source.events():
                row = "|".join(RowsDocument.function(event[k]) for k in keys)
                target.write(row)
