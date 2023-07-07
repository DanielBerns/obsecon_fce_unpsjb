from pathlib import Path
from typing import List

from parsel import Selector


class TextReaderHTMLWithParsel:
    def __init__(self):
        pass

    def read(self, resource: Path) -> List:
        with open(resource, "r") as source:
            html = source.read()
            html_selector = Selector(text=str(html))
            clean_text = self.extract(html_selector)
        return [clean_text]

    def extract(self, html_selector: Selector) -> str:
        body = html_selector.css('body')
        return clean_text.get()  # text.encode('utf-8')
