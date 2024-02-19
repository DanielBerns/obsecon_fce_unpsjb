import logging
import random
from typing import Dict
from pathlib import Path

from context import components, TEST_ROOT
from components.configuration import (CLI, Settings, Constants)
from components.helpers import (get_home, get_resource_with_timestamp, show)
from components.core import (application, create_application)

import unittest

PROJECT: str = Constants.PROJECT
VERSION: str = Constants.VERSION
MODE: str = "dev"
APPLICATION: str = "test_configuration"

class ConfigurationTestCase(unittest.TestCase):

    def setUp(self):
        print("setup")
        
    def tearDown(self):
        print("teardown")
        
    def test_application(self):
        application_name = "test_an_application"
        cli = CLI()
        cli.add_arguments(
            "-d",
            "--dotenv",
            type=str,
            default=".env", required=False,
            help="name of dotenv file",
        )    
        cli.add_arguments(
             "-m",
             "--mode",
             choices=["dev", "test", "live"],
             type=str,
             default="live", required=False,
             help="how to run? dev, test or live",
        )
        arguments = cli.arguments
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 1")   
            fs = application.file_system
            print(str(fs.info_home))
            print(str(fs.storage))
            print(str(fs.secrets))
            print(str(fs.results))
            print(str(fs.reports))
            print(str(fs.logs))            
            print(str(fs.software_home))
            print(str(fs.templates))
            print(str(fs.metadata.directory))
            print(str(application.settings))
            show(f"{application_name:s} 2")
        show(f"{application_name:s} 3")
    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
