import logging
import sys 

from config import Config, ConfigError, APPLICATION, VERSION
from components.core import Metadata, FileSystem
from components.helpers import get_container
import components.telegram_agent as telegram
import components.twitter_agent as twitter



def create_metadata(fs: FileSystem):
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()

def main():
    log_level = Config.get_log_level()
    # log_format = "%(levelname)s %(asctime)s - %(message)s"
    
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    
    logger.info("Start")            
    fs = FileSystem(Config.ROOT, APPLICATION, VERSION, Config.INSTANCE)
    logger.info("<FileSystem")
    logger.info(f":  home={str(fs.home):s}")
    logger.info(f"Filesystem>")
    logger.info("<metadata")        
    create_metadata(fs)
    logger.info("metadata>")    
    logger.info("Done")

if __name__ == '__main__':
    main()
