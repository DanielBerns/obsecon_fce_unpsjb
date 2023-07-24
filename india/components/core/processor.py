from typing import Dict, List

class Processor:
    def __init__(self):
        self._content: List = list()
        self._attributes: Dict[str, str] = dict()
        
    @property
    def content(self) -> List:
        return self._content
    
    @property
    def attributes(self) -> Dict[str, str]:
        return self._attributes
    
    def execute(self) -> None:
        pass
