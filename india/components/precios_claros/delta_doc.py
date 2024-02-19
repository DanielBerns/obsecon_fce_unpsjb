from typing import Protocol, List, Tuple
from pathlib import Path


class DeltaDoc(Protocol):
    @property
    def suffix(self) -> str:
        ...

    def header(self, 
               first_row: List[str], 
               second_row: List[str]) -> None:
        ...
        
    def card(self, 
             first_row: List[str], 
             second_row: List[Tuple[str, str]]) -> None:
        ...

    def footer(self) -> None:
        ...
        
    def write(self, resource: Path) -> None:
        ...
 
