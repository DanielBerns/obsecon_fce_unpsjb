import logging

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier
from components.logs import add_stdout_handler, add_file_handler

from components.twitter_agent import run, IDENTIFIER


def start():
    logger = logging.getLogger(f"{__name__:s}.{IDENTIFIER:s}")    
    config = Config()
    fs = FileSystem(config.home)
    logs_txt = get_resource_identifier(fs.logs, "logs", ".txt")    
    if config.log_stdout == "YES":    
        add_stdout_handler(logger, logging_level=config.log_stdout_level)
    add_file_handler(logger, logs_txt, logging_level=config.log_file_level)            
    logger.setLevel(logging.DEBUG)
    logger.info("Start")
    return config, fs, logger

 
def main():
    config, fs, logger = start()
    twitter_home = get_container(fs.data, IDENTIFIER)
    run(twitter_home, config.authorization_token[IDENTIFIER])

    
if __name__ == '__main__':
    main()
