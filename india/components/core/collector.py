from collections import Counter
from typing import Dict, Tuple, List


class Collector:
    def __init__(self, label: str, attributes: Tuple[str, ...]) -> None:
        self._label = label
        self._attributes = attributes
        self._counters = Counter()

    @property
    def label(self) -> str:
        return self._label
        
    @property
    def attributes(self) -> Tuple[str, ...]:
        return self._attributes
    
    @property
    def counters(self) -> Counter:
        return self._counters

    @property
    def attributes(self) -> Tuple[str, ...]:
        return self._attributes
    
    def update(self, event: Dict[str, str]):
        try:
            key = tuple(event[aa] for aa in self.attributes)
        except KeyError as message:
            key = ('bad_key', str(message))
        self.counters[key] += 1

    def keys_and_counts(self) -> List[Tuple[Tuple[str, ...], int]]:
        return sorted(((key, count) for key, count in self.table.items()), lambda x: x[1])

 
