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

# https://jsonlines.org/
from components.helpers import get_container, get_resource

from components.core.events import EventsDocument


class RowsDocument:
    adapter = lambda v: str(int(v * 100)) if isinstance(v, float) else str(v).lower()

    def __init__(self, container: Path) -> None:
        self._container: Path = container
        self._store: Path = get_resource(self.container, "store", ".csv")

    @property
    def container(self) -> Path:
        return self._container

    @property
    def store(self) -> Path:
        return self._store

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def rows(self) -> Generator[str, None, None]:
        with open(self.store, "r", encoding="utf-8") as origin:
            for line in origin:
                yield line

    def write(self, origin: EventsDocument) -> None:
        keys = origin.events_stats.keys()
        header = "|".join(str(k) for k in keys)
        with open(self.store, "w", encoding="utf-8") as target:
            target.write(header + "\n")
            for event in origin.events():
                row = "|".join(RowsDocument.adapter(event[k]) for k in keys)
                target.write(row)
