from typing import List
from pathlib import Path

import easyocr

class EasyOCRTextReader:
    def __init__(self, languages: List[str]):
        self._reader = easyocr.Reader(languages)
        
    def read_text(self, resource: Path) -> List:
        return self._reader.readtext(str(resource))    
