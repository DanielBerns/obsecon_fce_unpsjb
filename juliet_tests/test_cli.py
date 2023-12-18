import logging
import random
from typing import Dict
from pathlib import Path

from context import components, TEST_ROOT
from components.configuration import CLI, Constants
from components.helpers import (get_home, 
                                get_resource_with_timestamp)

import unittest

PROJECT: str = Constants.PROJECT
VERSION: str = Constants.VERSION
MODE: str = "dev"
APPLICATION: str = "test_cli"

class CLITestCase(unittest.TestCase):

    def setUp(self):
        logs = get_home(TEST_ROOT, 
                        PROJECT, VERSION, MODE, APPLICATION)
        logs_txt = get_resource_with_timestamp(logs, "test", ".txt")
        logging.basicConfig(
            filename=logs_txt, 
            level=logging.INFO
        )
        print(f"{APPLICATION:s} setUp")
        print(f"Logging at {str(logs_txt):s}")
        
    def tearDown(self):
        print(f"{APPLICATION:s} tearDown")
        
    def test_cli(self):
        logging.info(f"{APPLICATION:s} start")        
        cli = CLI()
        cli.add_arguments(
             "-m",
             "--mode",
             choices=["dev", "test", "live"],
             type=str,
             default="live", required=False,
             help="how to run? dev, test or live",
        )
        arguments = cli.arguments
        for key, value in arguments.items():
            print(f"{key:s} = {str(value):s}")
        logging.info(f"{APPLICATION:s} stop")    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
