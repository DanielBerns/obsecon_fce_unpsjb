import subprocess
import logging
from pathlib import Path
from typing import List
from random import randint

def _execute_command(minutes: int, command: Path) -> None:
    cp = subprocess.run(
        [
            "at",
            "now",
            f"+{minutes:d}",
            "minutes",
            "-f",
            str(command),
        ]
    )
    if cp.returncode:
        logging.error(f"at returncode {cp.returncode:d}")
 

def execute_commands(
    commands: List[Path], 
    a: int = 1, 
    b: int = 10
    ) -> None:
    a = 1 if a < 0 else a
    b = 10 if b < a else b
    for a_command in commands:
        this_command = a_command.expanduser()
        if this_command.exists() and this_command.is_file():
            minutes = randint(a, b)
            _execute_command(minutes, a_command)
