import logging

import sys 

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier
from components.logs import add_stdout_handler, add_file_handler


def start():
    logger = logging.getLogger(__name__)    
    config = Config()
    fs = FileSystem(config.home)
    logs_txt = get_resource_identifier(fs.logs, "logs", ".txt")    
    if config.log_stdout == "YES":    
        add_stdout_handler(logger, logging_level=config.log_stdout_level)
    add_file_handler(logger, logs_txt, logging_level=config.log_file_level)            
    logger.setLevel(logging.DEBUG)
    logger.info("Start")
    return config, fs, logger


def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()


def main():    
    config, fs, logger = start()    
    twitter_home = get_container(fs.data, 'twitter')
    telegram_home = get_container(fs.data, 'telegram')
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
