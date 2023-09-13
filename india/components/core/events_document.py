import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import DefaultDict, List, Dict, Protocol, Generator, Any

from components.helpers import get_directory, get_resource

import pdb

class EventsSource(Protocol):
    def events(self) -> Generator[Dict[Any, Any], None, None]:
        yield from ()


class EventsStatsError(Exception):
    pass


class EventsStats:
    def __init__(self) -> None:
        self._counters: DefaultDict[Any, Counter] = defaultdict(Counter)

    @property
    def counters(self) -> DefaultDict[Any, Counter]:
        return self._counters

    def update(self, event: Dict[Any, Any]) -> None:
        for key, value in event.items():
            self.counters[key]["total"] += 1
            value_type = type(value).__name__
            self.counters[key][value_type] += 1

    def keys(self) -> List[str]:
        p = [count["total"] for key, count in self.counters.items()]
        test_p = all([v == p[0] for v in p])
        if not test_p:
            raise EventsStatsError("EventStats.keys: bad stats events (not p).")
        q = [len(count.keys()) == 2 for key, count in self.counters.items()]
        test_q = all(q)
        if not test_q:
            raise EventsStatsError("EventStats.keys: bad stats events (not q).")
        return [key for key in self.counters.keys()]


class EventsDocument:
    
    @staticmethod
    def lower_values(event: Dict[str,Any]) -> Dict[str, str]:
        return {key: str(value).lower() for key, value in event.items()}
            
    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = get_resource(self.directory, "store", ".json")
        self._events_stats = EventsStats()

    @property
    def directory(self) -> Path:
        return self._directory

    @property
    def store(self) -> Path:
        return self._store

    @property
    def events_stats(self) -> EventsStats:
        return self._events_stats

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def events(self) -> Generator[Dict[Any, Any], None, None]:
        with open(self.store, "r", encoding="utf-8") as source:
            for line in source:
                event = json.loads(line)
                yield event

    def update(self, source: EventsSource) -> None:
        with open(self.store, "w", encoding="utf-8") as target:
            print(str(self.store))
            pdb.set_trace()
            for event in source.events():
                self.events_stats.update(event)
                line = json.dumps(event)
                target.write(f"{line:s}\n")
