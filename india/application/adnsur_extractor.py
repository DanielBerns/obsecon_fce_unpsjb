from typing import List

from bs4 import BeautifulSoup

from components.core import FileProcessor

class ContentExtractor(FileProcessor):
    def __init__(self) -> None:
        super().__init__()
        self._content = list()
        
    @property
    def content(self) -> List:
        return self._content
        
    def execute(self) -> None:
        with open(self.file_identifier, 'r') as source:
            text = source.read()
            self.extract_content(text)
            
    def extract_content(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")


class ADNSUR(ContentExtractor):
    def __init__(self) -> None:
        super().__init__()
        
    def execute(self) -> None:
        with open(self.file_identifier, 'r') as source:
            text = source.read()
            self.extract_content(text)
            
    def extract_content(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")

        find_spans_within_container_divs = [
            div.find_all("span") 
            for div in soup.find_all("div", class_="container")]
        for spans_within_container_div in find_spans_within_container_divs:
            for span in spans_within_container_div:
                if span:
                    for data in span.stripped_strings:
                        if data:
                            self.content.append((data,))
                    
        find_links_within_divs = [
            div.find_all("a") for div in soup.find_all("div")]
        for links_within_divs in find_links_within_divs:
            for link in links_within_divs:
                if link:
                    data = [text for text in link.stripped_strings]
                    if data:
                        for text in data:
                            if text:
                                self.content.append((text,))
                    text = link.get('aria-label', '')
                    if text:
                        self.content.append((text,))


class WebsiteExtractor(FileProcessor):
    """ADNSUR
    """
    def __init__(self) -> None:
        super().__init__()
        
    def execute(self) -> None:
        with open(self.file_identifier, 'r') as source:
            text = source.read()
            self.extract_content(text)
            
    def extract_content(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")
