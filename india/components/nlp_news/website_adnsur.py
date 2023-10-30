from typing import Any, Dict, List, Tuple
from pathlib import Path
from bs4 import BeautifulSoup

from components.core import SampleTask
from components.website_agent import GrabURLSample
from components.nlp import TextTXT, GetTextSampleTask


class ADNSURGetTextSampleTask(GetTextSampleTask):
    def __init__(self) -> None:
        super().__init__("adnsur")

    def start(self, target: Path) -> None:
        super().start(target)
    
    def stop(self, target: Path) -> None:
        super().stop(target)
    
    def execute(self, sample: Path) -> None:
        super().execute(sample)
        if self.text:
            self.text = list() 
        html, attributes = GrabURLSample.read(sample)
        soup = BeautifulSoup(html, "html.parser")

        find_spans_within_container_divs = [
            div.find_all("span") 
            for div in soup.find_all("div", class_="container")]
        for spans_within_container_div in find_spans_within_container_divs:
            for first_number, span in enumerate(spans_within_container_div):
                if span:                    
                    data = [text_fragment for text_fragment in span.stripped_strings]
                    if data:
                        self.text.append(("#span-start", f"#ff:{str(first_number):s}"))
                        for second_number, text_fragment in enumerate(data):
                            if text_fragment:
                                self.text.append((text_fragment, f"#ss:{str(second_number):s}"))
                        self.text.append(("#span-end",))            
                    
        find_links_within_divs = [
            div.find_all("a") for div in soup.find_all("div")]
        for links_within_divs in find_links_within_divs:                        
            for first_number, link in enumerate(links_within_divs):
                if link:
                    self.text.append(("#link-start", f"#ff:{str(first_number):s}"))                                        
                    data = [text_fragment for text_fragment in link.stripped_strings]
                    if data:
                        for second_number, text_fragment in enumerate(data):
                            if text_fragment:
                                self.text.append((text_fragment, f"#ss:{str(second_number):s}"))
                    text_fragment = link.get("aria-label", "")
                    if text_fragment:
                        self.text.append((text_fragment,"#aria-label"))
                    self.text.append(('#link-end',))
        TextTXT.write(sample, self.text)    

