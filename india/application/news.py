from application.adnsur_extractor import ADNSUR
from components.core import TextReaderHTMLWithParsel

def get_websites():
    websites = {}
    websites["adnsur"] = [
        ("https://adnsur.com.ar", ADNSUR())]
    websites["jornada"] = [
        ("https://www.diariojornada.com.ar/home", TextReaderHTMLWithParsel())]
    websites["cronica"] = [
        ("https://www.diariocronica.com.ar/", TextReaderHTMLWithParsel())]
    websites["elchubut"] = [
        ("https://www.elchubut.com.ar/seccion/comodoro-rivadavia", TextReaderHTMLWithParsel()),
        ("https://www.elchubut.com.ar/seccion/rawson", TextReaderHTMLWithParsel()),
        ("https://www.elchubut.com.ar/seccion/trelew", TextReaderHTMLWithParsel()),
        ("https://www.elchubut.com.ar/seccion/puerto-madryn", TextReaderHTMLWithParsel()),
        ("https://www.elchubut.com.ar/seccion/esquel", TextReaderHTMLWithParsel())
    ]
    websites["infobae"] = [
        ("https://www.infobae.com/", TextReaderHTMLWithParsel())]
 
