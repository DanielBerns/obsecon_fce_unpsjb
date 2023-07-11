from parsel import Selector

from components.core import TextReaderHTMLWithParsel

class ADNSUR(TextReaderHTMLWithParsel):
    def __init__(self):
        super().__init__()
        
    def extract(self, html_selector: Selector) -> str:
        div_container = html_selector.css('div.container')
        dollar = Selector(text=div_container[2].get())
        phrases = dollar.css('span.values')
        clean_text = '---'.join([item.get() for item in phrases])
        return clean_text  # text.encode('utf-8')
