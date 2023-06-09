from bs4 import BeautifulSoup

from typing import List, Tuple
from pathlib import Path 

class HTMLTextReader:
    def __init__(self):
        pass
        
    def read_text(self, resource: Path) -> List:
        with open(resource, 'r') as source:
            html = source.read()
            clean_text, noclean_text = self.extract_text(html)
        return [clean_text, noclean_text]
            
    def extract_text(self, html: str) -> Tuple[str, str]:
        soup = BeautifulSoup(html, "html.parser")
    
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
    
        # get noclean text
        noclean_text = soup.get_text("-xxx-")
        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in noclean_text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
    
        return clean_text, noclean_text # text.encode('utf-8')

    
