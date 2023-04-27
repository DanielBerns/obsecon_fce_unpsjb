#!/usr/bin/env python3
import os
import subprocess
import logging
import sys 
from pathlib import Path
from components.config import Config
from components.core import FileSystem
from components.helpers import get_container, get_resource_identifier, get_timestamp

DEFAULT_COMMAND = "*"

command = os.environ.get("COMMAND") or DEFAULT_COMMAND

if command == DEFAULT_COMMAND:
    sys.exit(1)

config = Config()
fs = FileSystem(config.home)
logs_edit_crontab_txt = get_resource_identifier(fs.logs, "edit_crontab", ".txt")
timestamp = get_timestamp()
filename = f"edit_crontab_{timestamp:s}"
logs_command_txt = get_resource_identifier(fs.logs, filename, ".txt")
logging.basicConfig(filename=logs_edit_crontab_txt, level=config.log_level)    
logging.info("start crontab edit")
crontab_home = get_container(fs.data, 'crontab')
crontab_update_txt = get_resource_identifier(crontab_home, 'crontab', '.txt')
command = str(Path(command).resolve())
logging.info(f"  command {command:s}")
with open(crontab_update_txt, 'w') as target:
     target.write(f'24 * * * * {command:s} >> {str(logs_command_txt):s} 2>&1\n')

cp = subprocess.run(['crontab', crontab_update_txt])

if cp.returncode:
    logging.info(f"crontab edit returncode {cp.returncode:d}")
logging.info("end crontab edit")    
