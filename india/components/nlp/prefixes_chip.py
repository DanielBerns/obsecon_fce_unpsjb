from typing import List

class PrefixesChip:
    
    @staticmethod
    def common_prefix(one: str, two: str) -> str:
        prefix = list()
        for a, b in zip(one, two):
            if a == b:
                prefix.append(a)
            else:
                break
        return ''.join(prefix)

    @staticmethod
    def get_prefixes(array: List[str]) -> List[str]:
        prefixes = list()                
        sorted_uniq = sorted(set(array))
        last_value = (sorted_uniq[0]).strip()
        for value in sorted_uniq[1:]:
            current_value = value.strip()
            prefix = PrefixesChip.common_prefix(current_value, last_value)
            last_value = current_value
            if prefix:
                if len(prefix) > 2:
                    prefixes.append(prefix.strip())
        return prefixes

    def __init__(self, lines: Optional[List[str]] = None) -> None:
        self._lines: List[str] = lines if lines else list()
        
    @property
    def lines(self) -> List[str]:
        return self._lines

    @property    
    def prefixes(self) -> None:
        return PrefixesChip.get_prefixes(self.lines)
