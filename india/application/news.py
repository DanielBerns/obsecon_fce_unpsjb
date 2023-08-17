from application.adnsur_extractor import ADNSURExtractorTask
from components.nlp import NLPTask, 
from components.core import EmptyTask
from components.website_agent import Website

EMPTY_PIPELINE = [EmptyTask(), EmptyTask()]
ADNSUR_PIPELINE = [ADNSURExtractorTask(), NLPTask()]

def get_websites():
    websites = {}
    websites.append(
        Website("adnsur", "https://adnsur.com.ar", ADNSUR_PIPELINE)
        )
    websites.append(
        Website("jornada", "https://www.diariojornada.com.ar/home", EMPTY_PIPELINE)
        )
    websites.append(
        Website("cronica", "https://www.diariocronica.com.ar/", EMPTY_PIPELINE)                
        )
    websites.append(
        Website("elchubut", "https://www.elchubut.com.ar/seccion/comodoro-rivadavia", EMPTY_PIPELINE)               
        )
    websites.append(
        Website("elchubut", "https://www.elchubut.com.ar/seccion/rawson", EMPTY_PIPELINE)                
        )
    websites.append(
        Website("elchubut", "https://www.elchubut.com.ar/seccion/trelew", EMPTY_PIPELINE)
        )
    websites.append(
        Website("elchubut", "https://www.elchubut.com.ar/seccion/puerto-madryn", EMPTY_PIPELINE)                
        )
    websites.append(
        Website("elchubut", "https://www.elchubut.com.ar/seccion/esquel", EMPTY_PIPELINE)
        )
    websites.append(
        Website("infobae", "https://www.infobae.com/", EMPTY_PIPELINE)
        )
    return websites
 
