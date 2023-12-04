import argparse
from typing import Dict

class CLI:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()
        
    @property
    def parser(self) -> argparse.ArgumentParser:
        return self._parser
    
    def arguments(self) -> Dict[str, str]:
        return vars(self.parser.parse_args())
 
    def add_arguments(self) -> None:
        self.parser.add_argument(
            "-m",
            "--mode",
            choices=["dev", "test", "live"],
            type=str,
            default="live", required=False,
            help="how to run? dev, test or live",
        )
