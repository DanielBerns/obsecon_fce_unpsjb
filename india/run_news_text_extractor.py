# test_extract_news_with_parsel

import logging

from application.engine import create_app
from components.core import TextReaderHTMLWithParsel
from components.website_agent import processor_run

IDENTIFIER = "test_extract_news_with_parsel"

import pdb

def main() -> None:
    websites = {}
    websites["adnsur"] = ["https://adnsur.com.ar"]
    websites["jornada"] = ["https://www.diariojornada.com.ar/home"]
    websites["cronica"] = ["https://www.diariocronica.com.ar/"]
    websites["elchubut"] = [
        "https://www.elchubut.com.ar/seccion/comodoro-rivadavia",
        "https://www.elchubut.com.ar/seccion/rawson",
        "https://www.elchubut.com.ar/seccion/trelew",
        "https://www.elchubut.com.ar/seccion/puerto-madryn",
        "https://www.elchubut.com.ar/seccion/esquel",
    ]
    websites["infobae"] = ["https://www.infobae.com/"]

    with create_app(IDENTIFIER) as app:
        text_reader = TextReaderHTMLWithParsel()
        pdb.set_trace()
        processor_run(app.fs.news, websites, app.fs.results, text_reader)


if __name__ == "__main__":
    main()
