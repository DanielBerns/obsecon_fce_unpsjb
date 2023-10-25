from typing import Dict, Optional

class CatalogException(Exception):
    pass

class Catalog:
    def __init__(self):
        self._table: Dict[str, Any] = {}
        
    @property
    def table(self) -> Dict[str, Any]:
        return self._table
        
    def create(self, key: str, value: Any) -> None:
        try:
            _ = self.table[key]
            raise CatalogException(
                f"{classname(self):s}.create")
        except KeyError:
            self.table[key] = value            
    
    def update(self, key: str, value: Any) -> None:
        try:
            _ = self._table[key]
            self.table[key] = value        
        except KeyError:
            raise CatalogException(
                f"{classname(self):s}.update")

    def delete(self, key: str) -> None:
        try:
            del self.table[key]
        except KeyError:
            raise CatalogException("delete")
            
    def get(self, key: str, on_key_error: Optional[Any] = None) -> Any:
        return self.table.get(key, on_key_error)
