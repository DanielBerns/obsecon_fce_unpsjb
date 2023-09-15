import json
from pathlib import Path
from collections import Counter, defaultdict
from typing import DefaultDict, List, Dict, Protocol, Generator, Any

from components.helpers import get_directory, get_resource


class Events:
    @staticmethod
    def lower_values(event: Dict[Any, Any]) -> Dict[str, str]:
        return {str(key): str(value).lower() for key, value in event.items()}


class EventsSource(Protocol):
    def events(self) -> Generator[Dict[Any, Any], None, None]:
        yield from ()


class EventProcessor(Protocol):
    def events(self, x: Dict[Any, Any]) -> Generator[Dict[Any, Any], None, None]
        yield from ()
     

class EventsException(Exception):
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

    def events(self) -> Generator[Dict[Any, Any], None, None]:
        with open(self.store, "r", encoding="utf-8") as source:
            for line in source:
                event = json.loads(line)
                yield event

    def update(self, source: EventsSource, mode="w") -> None:
        _mode = "a" if mode != "w" else "w"
        with open(self.store, _mode, encoding="utf-8") as target:
            print(str(self.store))
            for number, event in enumerate(source.events()):
                self.events_stats.update(event)
                line = json.dumps(event)
                target.write(f"{line:s}\n")
                if number % 100 == 1:
                    print(f"event #{number:d}")
                    
    
class CompositeEventsSource:
    def __init__(self) -> None:
        self._events_source: Optional[EventsSource] = None

    @property        
    def events_source(self) -> Optional[EventsSource]:
        return self._events_source
    
    @events_source.setter
    def events_source(self, value: EventsSource) -> None:
        self._events_source = value

    def events(self) -> Generator[Dict[Any, Any], None, None]:
        for event in self.events_source.events():
            yield event


class CompositeEventsDriver:
    def __init__(self) -> None:
        self._events_source: Optional[EventsSource] = None
        self._events_processor: Optional[EventsProcessor] = None

    @property        
    def events_source(self) -> Optional[EventsSource]:
        return self._events_source
    
    @events_source.setter
    def events_source(self, value: EventsSource) -> None:
        self._events_source = value

    @property        
    def events_processor(self) -> Optional[EventsProcessor]:
        return self._events_processor
    
    @events_processor.setter
    def events_processor(self, value: EventsProcessor) -> None:
        self._events_source = value

    def events(self) -> Generator[Dict[Any, Any], None, None]:
        for x in self.events_source.events():
            for event in self.events_processor.events(x):
                yield event


class SelectedEventsSource(CompositeEventsSource):
    def __init__(self):
        super().__init__()
    
    def select_event(self, event: Dict[Any, Any]) -> bool:
        # This is the base class
        # Change this in the child class
        return True

    def events(self) -> Dict[Any, Any]:
        for event in self.event_source.events():
            if self.select_event(event):
                yield event


class ProcessedEventsSource(CompositeEventsSource):
    def __init__(self):
        super().__init__()
    
    def process_event(self, event: Dict[Any, Any]) -> Dict[Any, Any]:
        # This is the base class
        # Change this in the child class
        return event

    def events(self) -> Dict[Any, Any]:
        for event in self.event_source.events():
            yield process_event(event)
