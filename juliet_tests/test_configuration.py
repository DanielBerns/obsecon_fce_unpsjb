import logging
import random
from typing import Dict
from pathlib import Path

from context import components, TEST_ROOT
from components.configuration import Settings, Constants
from components.helpers import (get_home, 
                                get_resource_with_timestamp)

import unittest

PROJECT: str = Constants.PROJECT
VERSION: str = Constants.VERSION
MODE: str = "dev"
APPLICATION: str = "test_configuration"

class ConfigurationTestCase(unittest.TestCase):

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
        
    def test_configuration(self):
        logging.info(f"{APPLICATION:s} start")        
        settings: Dict[str, str] = Settings.build(
            PROJECT, VERSION, MODE, APPLICATION, ".env")
        print("# settings")
        for key, value in settings.items():
            print(f"   {key:s}: {value:s}")
        logging.info(f"{APPLICATION:s} stop")    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
