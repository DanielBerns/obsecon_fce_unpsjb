from typing import Any, Dict, List, Tuple
from pathlib import Path
from bs4 import BeautifulSoup

from components.core import SampleTask
from components.helpers import read_text, load_json
from components.nlp.formats import NewsSample, TextTXT, CharactersMD, TokensMD


class ADNSURGetText(SampleTask):
    def __init__(self) -> None:
        super().__init__("adnsur")
        self._content: List[Any] = list()
        
    @property
    def content(self) -> List[Any]:
        return self._content
    
    @content.setter
    def content(self, value: List[Any]) -> None:
        self._content = value
    
    def execute(self, sample: Path) -> None:
        super().execute(sample)
        if self.content:
            self.content = list() 
        html, attributes = NewsSample.read(sample)
        soup = BeautifulSoup(html, "html.parser")

        find_spans_within_container_divs = [
            div.find_all("span") 
            for div in soup.find_all("div", class_="container")]
        for spans_within_container_div in find_spans_within_container_divs:
            for first_number, span in enumerate(spans_within_container_div):
                if span:                    
                    data = [text for text in span.stripped_strings]
                    if data:
                        self.content.append(("#span-start", f"#ff:{str(first_number):s}"))
                        for second_number, text in enumerate(data):
                            if text:
                                self.content.append((text, f"#ss:{str(second_number):s}"))
                        self.content.append(("#span-end",))            
                    
        find_links_within_divs = [
            div.find_all("a") for div in soup.find_all("div")]
        for links_within_divs in find_links_within_divs:                        
            for first_number, link in enumerate(links_within_divs):
                if link:
                    self.content.append(("#link-start", f"#ff:{str(first_number):s}"))                                        
                    data = [text for text in link.stripped_strings]
                    if data:
                        for second_number, text in enumerate(data):
                            if text:
                                self.content.append((text, f"#ss:{str(second_number):s}"))
                    text = link.get("aria-label", "")
                    if text:
                        self.content.append((text,"#aria-label"))
                    self.content.append(('#link-end',))
        TextTXT.write(sample, self.content)    
    
    def report(self, target: Path) -> None:
        super().report(target)
