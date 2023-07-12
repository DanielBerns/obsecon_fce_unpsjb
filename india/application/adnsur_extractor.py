from parsel import Selector

from components.core import TextReaderHTMLWithParsel

class ADNSUR(TextReaderHTMLWithParsel):
    """ADNSUR
    """
    def __init__(self):
        super().__init__()
        
    def extract(self, html_selector: Selector) -> str:
        div_container = html_selector.css('div.container')
        dollar = Selector(text=div_container[2].get())
        alpha = dollar.css('span.values')
        from_alpha = '---'.join([item.get() for item in alpha])
        bravo = html_selector.xpath('/html/body/div[6]/div/div/component-row')
        from_bravo = '---'.join([item.get() for item in bravo])
        return f"[{from_alpha:s}][{from_bravo:s}]"
