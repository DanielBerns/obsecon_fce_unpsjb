#!/usr/bin/env python3
import os
import subprocess
import logging
import sys 
from pathlib import Path
from components.config import Config
from components.core import FileSystem

IDENTIFIER = "edit_crontab"

DEFAULT_COMMANDS = "default_commands"

def main():
    config = Config()
    fs = FileSystem(config.application_home, config.info_home)
    logs_txt = fs.get_logs_resource(IDENTIFIER)
    logging.basicConfig(filename=logs_txt, level=config.log_level)    
    logging.info("start crontab edit")
    commands_txt = fs.get_commands_resource(DEFAULT_COMMANDS)
    crontab_update_txt, logs_crontab_txt = fs.get_crontab_resource()
    with open(commands_txt, 'r') as source, \
         open(crontab_update_txt, 'w') as target:
            for line in source:
                line_parts = (line[:-1]).split(':')
                if len(line_parts) == 2:
                    this_command = Path(line_parts[0]).expanduser()
                    this_time = line_parts[1]
                    this_time_parts = this_time.split(' ')
                    if len(this_time_parts) == 5:
                        for p in this_time_parts:
                            target.write(f'{p:s} ')
                        target.write(f'{str(this_command):s} >> {str(logs_crontab_txt):s} 2>&1\n')
                    else:
                        logging.warning(f'Error in {str(commands_txt):s} at {line:s}')
                else:
                    logging.warning(f'Error in {str(commands_txt):s} at {line:s}')                    
    cp = subprocess.run(['crontab', crontab_update_txt])
    
    if cp.returncode:
        logging.info(f"crontab edit returncode {cp.returncode:d}")
    logging.info("end crontab edit")    

if __name__ == "__main__":
    main()
