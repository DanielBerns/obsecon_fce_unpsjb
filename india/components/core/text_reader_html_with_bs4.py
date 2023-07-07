from pathlib import Path
from typing import List

from bs4 import BeautifulSoup


class TextReaderHTMLWithBS4:
    def __init__(self):
        pass

    def read(self, resource: Path) -> List:
        with open(resource, "r") as source:
            html = source.read()
            soup = BeautifulSoup(html, "html.parser")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            clean_text = self.extract_clean_text(soup)
        return [clean_text]

    def extract_clean_text(self, soup: BeatifulSoup) -> str:
        # get noclean text
        noclean_text = soup.get_text("-xxx-")        
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in noclean_text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        clean_text = "\n".join(chunk for chunk in chunks if chunk)

        return clean_text  # text.encode('utf-8')
