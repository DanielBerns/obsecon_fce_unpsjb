import subprocess
from pathlib import Path
from typing import List

def _execute_command(minutes: int, command_path: Path) -> None:
    cp = subprocess.run(
        [
            "at",
            "now",
            f"+{minutes:d}",
            "minutes",
            "-f",
            str(command_path),
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
        if a_command.exists() and a_command.is_file():
            minutes = random.randint(a, b)
            _execute_command(minutes, a_command)
