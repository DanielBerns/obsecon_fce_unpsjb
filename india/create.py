import logging

import sys 

from components.config import Config, APPLICATION, VERSION
from components.core import Metadata, FileSystem
from components.helpers import get_container
from components.logs import add_stdout_handler



def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()

def main():
    config = Config()
    logger = logging.getLogger(__name__)
    add_stdout_handler(logger)
    logger.setLevel(config.log_level)
    logger.info("Start")            
    fs = FileSystem(config.home)
    logger.info("<FileSystem>")
    logger.info(f":  home={str(fs.home):s}")
    logger.info("</Filesystem>")
    logger.info("<Metadata>")        
    create_metadata(fs)
    logger.info("</metadata>")    
    logger.info("Done")

if __name__ == '__main__':
    main()
