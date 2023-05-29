#!/usr/bin/env python3
import os
import subprocess
import logging
import sys 
from pathlib import Path

from app.engine import Engine

IDENTIFIER = "edit_crontab"

DEFAULT_COMMANDS = "default_commands"

class UpdateCrontabWarning(Exception):
    pass

def update_crontab(engine: Engine):
    commands_txt = engine.get_commands_resource(DEFAULT_COMMANDS)
    crontab_txt = engine.get_crontab_resource()
    with open(commands_txt, 'r') as source, \
         open(crontab_txt, 'w') as target:
            for line in source:
                line_parts = (line[:-1]).split(',')
                if len(line_parts) == 2:
                    command_bash, log_identifier = line_parts[0], line_parts[1]
                    command_bash_parts = command_bash.split(':')
                    if len(command_bash_parts) == 2:
                        this_command = Path(command_bash_parts).expanduser()
                        this_time = command_bash_parts[1]
                        this_time_parts = this_time.split(' ')
                        command_log = log_identifier[1:-1] if len(log_identifier) > 2 else 'command_log'
                        command_log_txt = engine.get_logs_resource(command_log)
                        if len(this_time_parts) == 5:
                            for p in this_time_parts:
                                target.write(f'{p:s} ')
                            target.write(f'{str(this_command):s} 2 > {str(command_log_txt):s} 2>&1\n')
                        else:
                            logging.warning(f'Error in {str(commands_txt):s} at {line:s}')
                            logging.warning('  I can not understand scheduled time')
                            raise UpdateCrontabWarning(f'Check {str(commands_txt):s}')
                    else:
                        logging.warning(f'Error in {str(commands_txt):s} at {line:s}')
                        logging.warning('  character ":" not founded')                        
                        raise UpdateCrontabWarning(f'Check {str(commands_txt):s}')
                else:
                    logging.warning(f'Error in {str(commands_txt):s} at {line:s}')             
                    logging.warning('  character "," not founded')                        
                    raise UpdateCrontabWarning(f'Check {str(commands_txt):s}')
    cp = subprocess.run(['crontab', crontab_update_txt])
    if cp.returncode:
        logging.info(f"crontab edit returncode {cp.returncode:d}")


def main():
    engine = Engine()
    
    logging.basicConfig(
        filename=engine.get_logs_resource(IDENTIFIER), 
        level=engine.config.log_level)    
    
    logging.info(f"start {IDENTIFIER:s}")

    try:
        update_crontab(engine)
    except UpdateCrontabWarning as message:
        logging.warning(str(message))

    logging.info(f"stop {IDENTIFIER:s}")

if __name__ == "__main__":
    main()
