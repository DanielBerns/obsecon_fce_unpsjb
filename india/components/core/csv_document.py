from collections import defaultdict, Counter
import json
import os
from pathlib import Path
from typing import List, Dict, Protocol, Union, Optional, Tuple, DefaultDict

from helpers import get_directory

class JSON2CSVError(Exception):
    pass

class EventsStats:
    def __init__(self) -> None:
        self._counters = defaultdict(Counter)
        
    @property
    def counters(self) -> defaultdict(Counter):
        return self._counters

    def update(self, event: Dict) -> None:
        for key, value in event.items():
            self.counters[key]['total'] += 1
            value_type = type(value).__name__
            self.counters[key][value_type] += 1
    
    def keys(self) -> List[str]:
        p = [count['total'] for key, count in self.counters.items()]
        test_p = all([v == p[0] for v in p])
        if not test_p:
            raise JSON2CSVError('EventStats.keys: bad stats events (not p).')
        q = [len(count.keys()) == 2 for key, count in self.counters.items()]
        test_q = all(q)                                                    
        if not test_q:
            raise JSON2CSVError('EventStats.keys: bad stats events (not q).')
        return [key for key in self.counters.keys()]


class CSVDocument:

    function = lambda v: str(int(v * 100)) if isinstance(v, float) else str(v).lower()
    
    def __init__(self, directory: Path) -> None:
        self._directory: Path = get_directory(directory)
        self._store: Path = Path(self.directory, 'store').with_suffix('.csv')
        
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
    
    def rows(self) -> str:
        with open(self.store, 'r') as source:
            header = source.readline()
            yield header
            for line in source:
                yield line
            
    def write(self, source: JSONDocument) -> None:
        events_stats = EventsStats()
        for event in source.get_events():
            events_stats.update(event)
        keys = events_stats.keys()
        header = '|'.join(keys)        
        with open(self.store, 'w') as target:
            target.write(header + '\n')
            for event in source.get_events():
                row = '|'.[CSVDocument.function(event[k]) for k in keys]

