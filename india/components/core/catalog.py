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
            raise CatalogException("create")
        except KeyError:
            self.table[key] = value            
    
    def update(self, key: str, value: Any) -> None:
        try:
            _ = self._table[key]
            self.table[key] = value        
        except KeyError:
            raise CatalogException("update")

    def delete(self, key: str) -> None:
        try:
            del self.table[key]
        except KeyError:
            raise CatalogException("delete")
            
    def get(self, key: str, on_key_error: Optional[Any] = None) -> Any:
        try:
            value = self._table[key]
            return value
        except KeyError:
            return on_key_error
