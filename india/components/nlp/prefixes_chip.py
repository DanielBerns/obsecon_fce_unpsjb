from typing import List, Optional

class PrefixesChip:
    @staticmethod
    def common_prefix(one: str, two: str) -> str:
        """Finds the longest common prefix of two strings."""
        i = 0
        while i < len(one) and i < len(two) and one[i] == two[i]:
            i += 1
        return one[:i]  # Return the prefix directly

    @staticmethod
    def get_prefixes(array: List[str]) -> List[str]:
        """Extracts common prefixes from a list of strings."""
        prefixes = []
        sorted_uniq = sorted(set(value.strip() for value in array))

        # Handle cases with less than two unique strings
        if len(sorted_uniq) < 2:
            return prefixes

        # Iterate through consecutive pairs of sorted strings
        for i in range(1, len(sorted_uniq)):
            prefix = PrefixesChip.common_prefix(sorted_uniq[i - 1], sorted_uniq[i])
            if prefix and len(prefix) > 2:
                prefixes.append(prefix)

        return prefixes

    def __init__(self, lines: Optional[List[str]] = None) -> None:
        self._lines: List[str] = lines if lines else []

    @property
    def lines(self) -> List[str]:
        return self._lines

    @property
    def prefixes(self) -> List[str]:
        """Returns the list of common prefixes found in the lines."""
        return PrefixesChip.get_prefixes(self.lines)
