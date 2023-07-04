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
    
    bot_home = engine.news
    results_home = engine.fs.results
    logging.info("Going to execute processor_start")    
    processor = processor_start(bot_home)
    logging.info("Executed processor_start")    
    pdb.set_trace()
    text_reader = TextReaderHTMLWithParsel()
    logging.info("Going to execute processor_run")    
    processor_run(results_home, text_reader, processor)
    logging.info("Executed processor_run")        


if __name__ == '__main__':
    main()
