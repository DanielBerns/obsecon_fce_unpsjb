from typing import List, Tuple
from pathlib import Path


class Text:
    def __init__(self) -> None:
        self._lines: List[str] = []
        
    @property
    def lines(self) -> List[str]:
        return self._lines
    
    def write(self, resource: Path) -> None:
        with open(resource, 'w') as target:
            for a_line in self.lines:
                target.write(f"{a_line.strip():s}\n")


class HTMLDeltaDoc:

    @staticmethod
    def prolog() -> str:
        return """
            <!DOCTYPE html>
            <html lang="es-ar">
            <title>Variación de precios</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
            <style>
              .name {
                 white-space: nowrap;
                 overflow: hidden;
                 text-overflow: ellipsis;
                 background-color: #DDFFFF;
              }
            </style>
            <body>
            <div class="w3-container w3-light-grey">
                 <h1>Variación de precios</h1>
        """
    @staticmethod        
    def header_row(content: List[str]) -> str:
        return f"""
            <div class="w3-row w3-teal">
              <div class="w3-col s12">{content[0]:s}</div>
              <div class="w3-col s4  w3-right-align">{content[1]:s}</div>
              <div class="w3-col s4  w3-right-align">{content[2]:s}</div>
              <div class="w3-col s4  w3-right-align">{content[3]:s}</div>            
            </div>
        """
    
    @staticmethod    
    def card_first_row(content: List[str]) -> str:
        return f"""
              <div class="w3-row">
                  <div class="w3-col s12 name">{content[0]:s}</div>
                  <div class="w3-col s4 w3-right-align">{content[1]:s}</div>
                  <div class="w3-col s4 w3-right-align">{content[2]:s}</div>
                  <div class="w3-col s4 w3-right-align">{content[3]:s}</div>            
              </div>
        """

    @staticmethod        
    def card_second_row(content: List[Tuple[str, str]]) -> str: 
        return f"""
                <div class="w3-row">
                  <div class="w3-col s12"></div>
                  <div class="w3-col s4 w3-right-align" style="background-color:#{content[1][1]:s};">{content[1][0]:s}</div>
                  <div class="w3-col s4 w3-right-align" style="background-color:#{content[2][1]:s};">{content[2][0]:s}</div>
                  <div class="w3-col s4 w3-right-align" style="background-color:#{content[3][1]:s};">{content[3][0]:s}</div>            
                </div>
        """

    @staticmethod        
    def epilog() -> str:
        return """</div></body></html>"""
      
    def __init__(self) -> None:
        self._suffix = ".html"        
        self._text: Text = Text()
        self.text.lines.append(HTMLDeltaDoc.prolog())

    @property
    def suffix(self) -> str:
        return self._suffix

    @property
    def text(self) -> Text:
        return self._text

    def header(self, 
               first_row: List[str], 
               second_row: List[str]) -> None:
        self.text.lines.append(HTMLDeltaDoc.header_row(first_row))
        self.text.lines.append(HTMLDeltaDoc.header_row(second_row))
    
    def card(self, 
             first_row: List[str], 
             second_row: List[Tuple[str, str]]) -> None:
        self.text.lines.append(HTMLDeltaDoc.card_first_row(first_row))
        self.text.lines.append(HTMLDeltaDoc.card_second_row(second_row))

    def footer(self) -> None:
        self.text.lines.append(HTMLDeltaDoc.epilog())

    def write(self, resource: Path) -> None:
        self.text.write(resource.with_suffix(self.suffix))
 
