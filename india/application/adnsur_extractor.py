from typing import List, TextIO

from bs4 import BeautifulSoup

from components.core import ContentProcessor

class ADNSUR(ContentProcessor):
    def __init__(self) -> None:
        super().__init__()
        
    def read(self, source: TextIO) -> None:
        self.content = []
        text = source.read()
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
            
    def write(self, target: TextIO) -> None:
        for datalist in self.content:
            for data in datalist:
                target.write(str(data) + "\n")


# class WebsiteExtractor(FileProcessor):
#     """
#     """
#     def __init__(self) -> None:
#         super().__init__()
#         
#     def execute(self) -> None:
#         with open(self.file_identifier, "r") as source:
#             text = source.read()
#             self.extract_content(text)
#             
#     def extract_content(self, text: str) -> None:
#         soup = BeautifulSoup(text, "html.parser")
