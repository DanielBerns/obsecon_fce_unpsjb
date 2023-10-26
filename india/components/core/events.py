import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import DefaultDict, List, Dict, Protocol, Generator, Optional

# import pdb

from components.helpers import get_directory, get_resource, classname

class Events:
    @staticmethod
    def lower_values(event: Dict[str, str]) -> Dict[str, str]:
        return {str(key): str(value).lower() for key, value in event.items()}


class EventsOrigin(Protocol):
    def events(self) -> Generator[Dict[str, str], None, None]:
        yield from ()


class EventsProcessor(Protocol):
    def events(self, x: Dict[str, str]) -> Generator[Dict[str, str], None, None]:
        yield from ()
     

class EventsException(Exception):
    pass


class EventsStats:
    def __init__(self) -> None:
        self._counters: DefaultDict[str, Counter] = defaultdict(Counter)

    @property
    def counters(self) -> DefaultDict[str, Counter]:
        return self._counters

    def update(self, event: Dict[str, str]) -> None:
        for key, value in event.items():
            self.counters[key]["total"] += 1
            value_type = type(value).__name__
            self.counters[key][value_type] += 1

    def keys(self) -> List[str]:
        p = [count["total"] for key, count in self.counters.items()]
        test_p = all([v == p[0] for v in p])
        if not test_p:
            raise EventsException("EventStats.keys: bad stats events (not p).")
        q = [len(count.keys()) == 2 for key, count in self.counters.items()]
        test_q = all(q)
        if not test_q:
            raise EventsException("EventStats.keys: bad stats events (not q).")
        return [key for key in self.counters.keys()]


    
class EventsDocument:
            
    def __init__(self, 
                 directory: Path, 
                 name: str = "store",
                 suffix: str = ".json") -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = get_resource(self.directory, name, suffix)
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

    def events(self) -> Generator[Dict[str, str], None, None]:
        with open(self.store, "r", encoding="utf-8") as origin:
            for line in origin:
                event = json.loads(line)
                yield event

    def update(self, origin: EventsOrigin, mode="w") -> None:
        _mode = "a" if mode != "w" else "w"
        with open(self.store, _mode, encoding="utf-8") as target:
            print(str(self.store))
            for number, event in enumerate(origin.events()):
                self.events_stats.update(event)
                line = json.dumps(event)
                target.write(f"{line:s}\n")
                if number % 100 == 1:
                    print(f"{classname(self):s} event #{number:d}")


class CompositeEventsOrigin:
    def __init__(self) -> None:
        self._events_origin: Optional[EventsOrigin] = None

    @property        
    def events_origin(self) -> Optional[EventsOrigin]:
        return self._events_origin
    
    @events_origin.setter
    def events_origin(self, value: EventsOrigin) -> None:
        self._events_origin = value

    def events(self) -> Generator[Dict[str, str], None, None]:
        for event in self.events_origin.events():
            yield event


class CompositeEventsDriver:
    def __init__(self) -> None:
        self._events_origin: Optional[EventsOrigin] = None
        self._events_processor: Optional[EventsProcessor] = None

    @property        
    def events_origin(self) -> Optional[EventsOrigin]:
        return self._events_origin
    
    @events_origin.setter
    def events_origin(self, value: EventsOrigin) -> None:
        self._events_origin = value

    @property        
    def events_processor(self) -> Optional[EventsProcessor]:
        return self._events_processor
    
    @events_processor.setter
    def events_processor(self, value: EventsProcessor) -> None:
        self._events_processor = value

    def events(self) -> Generator[Dict[str, str], None, None]:
        # pdb.set_trace()
        for x in self.events_origin.events():
            for event in self.events_processor.events(x):
                yield event


class SelectedEventsOrigin(CompositeEventsOrigin):
    def __init__(self):
        super().__init__()
    
    def select_event(self, event: Dict[str, str]) -> bool:
        # This is the base class
        # Change this in the child class
        return True

    def events(self) -> Dict[str, str]:
        for event in self.events_origin.events():
            if self.select_event(event):
                yield event


class ProcessedEventsOrigin(CompositeEventsOrigin):
    def __init__(self):
        super().__init__()
    
    def process_event(self, event: Dict[str, str]) -> Dict[str, str]:
        # This is the base class
        # Change this in the child class
        return event

    def events(self) -> Dict[str, str]:
        for event in self.events_origin.events():
            yield self.process_event(event)
