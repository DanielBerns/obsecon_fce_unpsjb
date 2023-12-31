from typing import Dict, Optional, TypeVar, Generic

class CatalogException(Exception):
    pass

T = TypeVar("T")

class Catalog(Generic[T]):
    def __init__(self):
        self._table: Dict[str, T] = {}  # Internal table for storing data

    @property
    def table(self) -> Dict[str, T]:
        """Returns a read-only view of the internal table."""
        return self._table.copy()  # Return a copy to prevent direct modification

    def create(self, key: str, value: T) -> None:
        """Creates a new entry in the catalog."""
        if key in self._table:
            raise CatalogException(f"Entry with key '{key}' already exists.")
        self._table[key] = value

    def update(self, key: str, value: T) -> None:
        """Updates an existing entry in the catalog."""
        if key not in self._table:
            raise CatalogException(f"Entry with key '{key}' not found.")
        self._table[key] = value

    def delete(self, key: str) -> None:
        """Deletes an entry from the catalog."""
        if key not in self._table:
            raise CatalogException(f"Entry with key '{key}' not found.")
        del self._table[key]

    def get(self, key: str, on_key_error: Optional[T] = None) -> T:
        """Retrieves an entry from the catalog."""
        return self._table.get(key, on_key_error)
