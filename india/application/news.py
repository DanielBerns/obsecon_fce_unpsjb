from typing import List

from application.adnsur import ADNSURGetText
from components.nlp import NLPGetTokens
from components.core import EmptySampleTask
from components.website_agent import Website

def get_websites() -> Dict[str, Tuple[str, ...]]:
    websites = {
    "adnsur": ("https://adnsur.com.ar",),
    "jornada": ("https://www.diariojornada.com.ar/home",),
    "cronica": ("https://www.diariocronica.com.ar/",),
    "elchubut": ("https://www.elchubut.com.ar/seccion/comodoro-rivadavia",),
    "elchubut": ("https://www.elchubut.com.ar/seccion/rawson", 
                 "https://www.elchubut.com.ar/seccion/trelew", 
                 "https://www.elchubut.com.ar/seccion/puerto-madryn",
                 "https://www.elchubut.com.ar/seccion/esquel",),
    "infobae": ("https://www.infobae.com/",)}
    return websites
 
