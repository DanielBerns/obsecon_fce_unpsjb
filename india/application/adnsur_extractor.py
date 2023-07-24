from bs4 import BeautifulSoup

from components.core import FileProcessor

import pdb

class ADNSUR(FileProcessor):
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

        find_spans_within_container_divs = [
            div.find_all("span") 
            for div in soup.find_all("div", class_="container")]
        for spans_within_container_div in find_spans_within_container_divs:
            for span in spans_within_container_div:
                if span:
                    pdb.set_trace()
                    self.content.append((span.text,""))
                    
        find_links_within_divs = [
            div.find_all("a") for div in soup.find_all("div")]
        for links_within_divs in find_links_within_divs:
            for link in links_within_divs:
                if link:
                    pdb.set_trace()
                    link_content = (link.text, link['aria-label']) \
                        if link.has_attr('aria-label') else (link.text,)
                    self.content.append(link_content)



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
