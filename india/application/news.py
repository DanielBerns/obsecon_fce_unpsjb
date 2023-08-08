from application.adnsur_extractor import ADNSUR
from components.core import FileProcessor


class DefaultExtractor(FileProcessor):
    """
    """
    def __init__(self) -> None:
        super().__init__()
        
    def execute(self) -> None:
        with open(self.file_identifier, 'r') as source:
            text = source.read()
            self.extract_content(text)
            
    def extract_content(self, text: str) -> None:
        soup = BeautifulSoup(text, "html.parser")

def get_websites():
    websites = {}
    websites["adnsur"] = [
        ("https://adnsur.com.ar", ADNSUR())]
    websites["jornada"] = [
        ("https://www.diariojornada.com.ar/home", DefaultExtractor())]
    websites["cronica"] = [
        ("https://www.diariocronica.com.ar/", DefaultExtractor())]
    websites["elchubut"] = [
        ("https://www.elchubut.com.ar/seccion/comodoro-rivadavia", DefaultExtractor()),
        ("https://www.elchubut.com.ar/seccion/rawson", DefaultExtractor()),
        ("https://www.elchubut.com.ar/seccion/trelew", DefaultExtractor()),
        ("https://www.elchubut.com.ar/seccion/puerto-madryn", DefaultExtractor()),
        ("https://www.elchubut.com.ar/seccion/esquel", DefaultExtractor())
    ]
    websites["infobae"] = [
        ("https://www.infobae.com/", DefaultExtractor())]
    return websites
 
