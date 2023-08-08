from typing import List
from components.core import FileProcessor

class ContentProcessor(FileProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._content = list()
        
    @property
    def content(self) -> List:
        return self._content

    @content.setter 
    def content(self, value: List):
        self._content = value
