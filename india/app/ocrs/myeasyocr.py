from app.text_reader import TextReader
import easyocr

class EasyOCR:
    def __init__(self, languages: List[str]):
        self._reader = easyocr.Reader(languages)
        
    def read_text(self, resource: Path) -> List:
        return self.reader.readtext(str(resource))    
