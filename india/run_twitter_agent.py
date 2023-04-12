import logging

from components.config import Config, APPLICATION, VERSION
from components.core import Metadata, FileSystem
from components.helpers import get_container
from components.logs import add_stdout_handler

from components.twitter_agent import run
 
def main():
    config = Config()
    logger = logging.getLogger(__name__)
    add_stdout_handler(logger)
    logger.setLevel(config.log_level)
    logger.info("Start")            
    fs = FileSystem(config.home)
    twitter_home = get_container(fs.data, 'twitter')
    run(twitter_home)
    
if __name__ == '__main__':
    main()
