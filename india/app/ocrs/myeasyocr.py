from typing import List
from pathlib import Path

import easyocr

from app.text_reader import TextReader


class EasyOCR:
    def __init__(self, languages: List[str]):
        self._reader = easyocr.Reader(languages)
        
    def read_text(self, resource: Path) -> List:
        return self.reader.readtext(str(resource))    
