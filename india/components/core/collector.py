from collections import Counter
from typing import Dict, Tuple, List, Any


class Collector:
    def __init__(self, label: str, attributes: Tuple[str, ...]) -> None:
        self._label = label
        self._attributes = attributes
        self._counters: Counter = Counter()

    @property
    def label(self) -> str:
        return self._label

    @property
    def attributes(self) -> Tuple[str, ...]:
        return self._attributes

    @property
    def counters(self) -> Counter:
        return self._counters

    def update(self, event: Dict[str, str]):
        key = list()
        for aa in self.attributes:
            vv = event.get(aa, None)
            if vv:
                key.append(vv)
        if key:
            self.counters[tuple(key)] += 1

    def keys_and_counts(self) -> List[Tuple[Any, int]]:
        items = ((key, count) for key, count in self.counters.items())
        return sorted(items, key=lambda x: x[1])
