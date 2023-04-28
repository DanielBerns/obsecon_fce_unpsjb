import logging

import sys 

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier
from components.logs import add_stdout_handler, add_file_handler


IDENTIFIER = "create"


def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()


def main():    
    config, fs, logger = start()    
    logs_txt = get_resource_identifier(fs.logs, IDENTIFIER, ".txt")
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")
    
    twitter_home = get_container(fs.data, 'twitter')
    telegram_home = get_container(fs.data, 'telegram')
    news_home = get_container(fs.data, 'news')
    logger.info("<FileSystem>")
    logger.info(f":  home={str(fs.home):s}")
    logger.info("</Filesystem>")
    logger.info("<Metadata>")        
    create_metadata(fs)
    logger.info("</Metadata>")
    logger.warning("THIS IS A TEST")
    logger.error("THIS IS ANOTHER TEST")
    logger.info("Done")

if __name__ == '__main__':
    main()
