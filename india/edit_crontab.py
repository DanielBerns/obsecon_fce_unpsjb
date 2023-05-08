#!/usr/bin/env python3
import os
import subprocess
import logging
import sys 
from pathlib import Path
from components.config import Config
from components.core import FileSystem
from components.helpers import (get_container,
                               get_resource_identifier,
                               get_timestamp)

NO_COMMAND = "*"

IDENTIFIER = "run_news_grabber"

def main():
    command = os.environ.get("COMMAND") or NO_COMMAND
    
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    timestamp = get_timestamp()
    logs_txt = get_resource_identifier(
        fs.logs, 
        f"{IDENTIFIER:s}_{timestamp:s}", 
        ".txt")    
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    if command == NO_COMMAND:
        logging.warning("No command to execute.")
        sys.exit(1)
    logging.info("start crontab edit")
    crontab_home = get_container(fs.data, 'crontab')
    crontab_update_txt = get_resource_identifier(crontab_home, 'crontab', '.txt')
    command = str(Path(command).resolve())
    logs_command_txt = get_resource_identifier(
        fs.logs, 
        f"command_{timestamp:s}", ".txt")
    logging.info(f"  command {command:s}")
    logging.info(f"  logs_command_txt {str(logs_command_txt):s}")
    with open(crontab_update_txt, 'w') as target:
         target.write(f'27 * * * * {command:s} >> {str(logs_command_txt):s} 2>&1\n')
    cp = subprocess.run(['crontab', crontab_update_txt])
    
    if cp.returncode:
        logging.info(f"crontab edit returncode {cp.returncode:d}")
    logging.info("end crontab edit")    

if __name__ == "__main__":
    main()
