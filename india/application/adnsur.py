from typing import List, Any
from pathlib import Path
from bs4 import BeautifulSoup

from components.helpers import read_text

class ADNSURSampleTask:
    def __init__(self) -> None:
        self._content: List[Any] = list()
        
    @property
    def content(self) -> List[Any]:
        return self._content
    
    @content.setter
    def content(self, value: List[Any]) -> None:
        self._content = value
    
    def execute(self, source: Path) -> None:
        if self.content:
            self.content = [] 
        text = read_text(Path(source, 'page.html'))
        soup = BeautifulSoup(text, "html.parser")

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
            
    def report(self, target: Path) -> None:
        with open(Path(target, 'text.txt'), 'w') as target:
            for event in self.content:
                for data in event:
                    target.write(str(data) + "\n")
