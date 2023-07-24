from application.adnsur_extractor import ADNSUR, WebsiteExtractor

def get_websites():
    websites = {}
    websites["adnsur"] = [
        ("https://adnsur.com.ar", ADNSUR())]
    websites["jornada"] = [
        ("https://www.diariojornada.com.ar/home", WebsiteExtractor())]
    websites["cronica"] = [
        ("https://www.diariocronica.com.ar/", WebsiteExtractor())]
    websites["elchubut"] = [
        ("https://www.elchubut.com.ar/seccion/comodoro-rivadavia", WebsiteExtractor()),
        ("https://www.elchubut.com.ar/seccion/rawson", WebsiteExtractor()),
        ("https://www.elchubut.com.ar/seccion/trelew", WebsiteExtractor()),
        ("https://www.elchubut.com.ar/seccion/puerto-madryn", WebsiteExtractor()),
        ("https://www.elchubut.com.ar/seccion/esquel", WebsiteExtractor())
    ]
    websites["infobae"] = [
        ("https://www.infobae.com/", WebsiteExtractor())]
    return websites
 
