from typing import Dict, Optional, TypeVar, Generic


class CatalogException(Exception):
    pass


T = TypeVar("T")


class Catalog(Generic[T]):
    def __init__(self):
        self._table: Dict[str, T] = {}

    @property
    def table(self) -> Dict[str, T]:
        return self._table

    def create(self, key: str, value: T) -> None:
        try:
            _ = self.table[key]
            raise CatalogException(f"{classname(self):s}.create")
        except KeyError:
            self.table[key] = value

    def update(self, key: str, value: T) -> None:
        try:
            _ = self._table[key]
            self.table[key] = value
        except KeyError:
            raise CatalogException(f"{classname(self):s}.update")

    def delete(self, key: str) -> None:
        try:
            del self.table[key]
        except KeyError:
            raise CatalogException("delete")

    def get(self, key: str, on_key_error: Optional[T] = None) -> T:
        return self.table.get(key, on_key_error)
