class Section:
    def __init__(self) -> None:
        pass
    
class Document:
    def __init__(self) -> None:
        self._title: str = ""
        self._sections: List[Section] = []
       
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        self._title = value
        
    @property
    def sections(self) -> List[Section]:
        return self._sections
    

class Processor:
    @staticmethod
    def add_section(document: Document, section: Section) -> Document:
        document.sections.append(section)
        return Document
        
    @staticmethod
    def create_section(
        article: Article, prices: List[int]) -> Section:
        
