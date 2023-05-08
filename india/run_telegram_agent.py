import logging

import sys 

from components.config import Config
from components.core import Metadata, FileSystem
from components.helpers import get_container, get_resource_identifier, get_timestamp
from components.logs import add_stdout_handler, add_file_handler

from components.telegram_agent import run


IDENTIFIER = "run_telegram_agent"


def main():
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    timestamp = get_timestamp()
    logs_txt = get_resource_identifier(
        fs.logs, f"{IDENTIFIER:s}_{timestamp:s}", ".txt")
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")

    run(fs.data, config.authorization_token["telegram"])


if __name__ == '__main__':
    main()
