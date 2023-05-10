import logging

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier
from components.logs import add_stdout_handler, add_file_handler

from components.website_agent import WebsiteAgent 


IDENTIFIER = "run_news_grabber"


def main():
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    logs_txt = fs.get_logs_resource(IDENTIFIER)
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")

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
    logging.info("start main")    
    logging.info(f">  data_home: {str(fs.data):s}")
    news = get_container(fs.data, 'news')
    for identifier, urls in websites.items():
        agent = WebsiteAgent(news, identifier)
        agent.grab_urls(urls)        
    logging.info("done main")

    
if __name__ == "__main__":
    main()
