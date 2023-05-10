import logging

import sys 

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier, get_timestamp


IDENTIFIER = "start"


def create_metadata(fs: FileSystem) -> None:
    container = get_container(fs.data, 'metadata')
    metadata = Metadata(container)
    metadata.start()
    metadata.stop()

DEFAULT_COMMANDS = [
  "~/Apps/observatorio_fce_unpsjb/india/run_news_grabber.sh:36 * * * *"
  "~/Apps/observatorio_fce_unpsjb/india/update_app.sh:37 * * * *"
]

def create_default_commands(fs: FileSystem) -> None:
    default_commands = fs.get_commands_resource("default_commands")
    with open(default_commands, 'w') as target:
        for line in DEFAULT_COMMANDS:
            target.write(f"{line:s}\n")
        
def main():    
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    timestamp = get_timestamp()
    logs_txt = fs.get_logs_resource(IDENTIFIER)
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
    logging.info("<Commands>")        
    create_default_commands(fs)
    logging.info("</Commands>")    
    logging.warning("THIS IS A TEST")
    logging.error("THIS IS ANOTHER TEST")
    logging.info("Done")

if __name__ == '__main__':
    main()
