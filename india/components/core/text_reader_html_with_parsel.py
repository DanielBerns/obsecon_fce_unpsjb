from pathlib import Path 
from typing import List, Tuple

from parsel import Selector

import pdb

class TextReaderHTMLWithParsel:
    def __init__(self):
        pass
        
    def read_text(self, resource: Path) -> List:
        with open(resource, 'r') as source:
            html = source.read()
            clean_text, noclean_text = self.extract_text(html)
        return [clean_text, noclean_text]
            
    def extract_text(self, html: str) -> Tuple[str, str]:
        html_selector = Selector(text=str(html))
        pdb.set_trace()
        noclean_text = "xxx"
        clean_text = "yyy"
    
        return clean_text, noclean_text # text.encode('utf-8')

    
