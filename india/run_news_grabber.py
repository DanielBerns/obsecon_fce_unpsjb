import logging

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier
from components.logs import add_stdout_handler, add_file_handler

from components.website_agent import WebsiteAgent 

IDENTIFIER = "news"


def start():
    logger = logging.getLogger(f"{__name__:s}.{IDENTIFIER:s}")    
    config = Config()
    fs = FileSystem(config.home)
    logs_txt = get_resource_identifier(fs.logs, "logs", ".txt")    
    if config.log_stdout == "YES":    
        add_stdout_handler(logger, logging_level=config.log_stdout_level)
    add_file_handler(logger, logs_txt, logging_level=config.log_file_level)            
    # logger.setLevel(logging.DEBUG)
    return config, fs, logger


def main():
    config, fs, logger = start()
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
    logger.info("start main")    
    logger.info(f">  home: {str(fs.home):s}")
    news_home = get_container(fs.data, 'news')
    for identifier, urls in websites.items():
        agent = WebsiteAgent(news_home, identifier)
        agent.grab_urls(urls)        
    logger.info("done main")

    
if __name__ == "__main__":
    main()
