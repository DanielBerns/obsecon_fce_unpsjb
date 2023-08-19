from collections import defaultdict
from typing import Dict, Tuple, List, Generator

# from mynlp.substrings.echo.py

def collect_common_strings(red: str, blue: str) -> Dict[str, List[Tuple[int, int]]]:
    collector = defaultdict(list)
    current = [0] * len(blue)
    index = [i for i in range(len(blue))]
    
    def next_step():
        update = [cc + 1 if dd == tt else 0 for cc, tt in zip(current, blue)]
        for cc, uu, ii in zip(current, update, index):
            if cc > 1 and uu == 0:
                key = blue[ii - cc: ii]
                collector[key].append((ii - cc, ii))

    for dd in red:
        next_step()
        current[0], current[1:] = 0, update[:-1]
    next_step()
    
    return collector


def list_collected_strings(
    collector: Dict[str, List[Tuple[int, int]]]
) -> Generator[Tuple[str, int, int], None, None]:
    for key, positions in collector.items():
        for start, stop in positions:
            yield key, start, stop
