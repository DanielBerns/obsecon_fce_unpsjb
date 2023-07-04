# test_extract_news_with_parsel

import logging

from app.engine import Engine
from components.core import TextReaderHTMLWithParsel
from components.website_agent import processor_start, processor_run

IDENTIFIER = "test_extract_news_with_parsel"

import pdb

def main() -> None:
    engine = Engine()
    logs_txt = engine.get_logs_resource(IDENTIFIER)
    logging.basicConfig(
        filename=logs_txt, 
        level=engine.config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")
    
    results_home = engine.fs.results
    websites = {}
    websites["adnsur"] = ["https://adnsur.com.ar"]
    websites["jornada"] = ["https://www.diariojornada.com.ar/home"]
    websites["cronica"] = ["https://www.diariocronica.com.ar/"]
    websites["elchubut"] = [
        "https://www.elchubut.com.ar/seccion/comodoro-rivadavia",
        "https://www.elchubut.com.ar/seccion/rawson",
        "https://www.elchubut.com.ar/seccion/trelew",
        "https://www.elchubut.com.ar/seccion/puerto-madryn",
        "https://www.elchubut.com.ar/seccion/esquel"]
    websites["infobae"] = ["https://www.infobae.com/"]

    text_reader = TextReaderHTMLWithParsel()
    
    for key, website in websites.items():
        logging.info("Going to execute processor_start")            
        processor = processor_start(engine.news, key)
        logging.info("Executed processor_start")    
        logging.info("Going to execute processor_run")    
        processor_run(results_home, text_reader, processor)
        logging.info("Executed processor_run")        


if __name__ == '__main__':
    main()
