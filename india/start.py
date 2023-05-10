import logging

import sys 

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier, get_timestamp


IDENTIFIER = "start"


def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()


def main():    
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    timestamp = get_timestamp()
    logs_txt = get_resource_identifier(
        fs.logs, 
        F"{IDENTIFIER:s}_{timestamp:s}", 
        ".txt")
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")
    
    twitter_home = get_container(fs.data, 'twitter')
    telegram_home = get_container(fs.data, 'telegram')
    news_home = get_container(fs.data, 'news')
    logging.info("<FileSystem>")
    logging.info(f":  application_home={str(fs.application_home):s}")
    logging.info(f":  info_home       ={str(fs.info_home):s}")    
    logging.info("</Filesystem>")
    logging.info("<Metadata>")        
    create_metadata(fs)
    logging.info("</Metadata>")
    logging.warning("THIS IS A TEST")
    logging.error("THIS IS ANOTHER TEST")
    logging.info("Done")

if __name__ == '__main__':
    main()
