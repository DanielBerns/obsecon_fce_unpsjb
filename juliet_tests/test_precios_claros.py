import logging
import random
from typing import Dict
from pathlib import Path

from context import components
from components.helpers import (get_home, get_resource_with_timestamp, show)
from components.core import create_application
from components.precios_claros import Actions

import pdb

import unittest

APPLICATION: str = "test_precios_claros"

class PreciosClarosTestCase(unittest.TestCase):

    def setUp(self):
        print("setup")
        
    def tearDown(self):
        print("teardown")
        
    def test_application(self):
        application_name = APPLICATION
        arguments = {"dotenv": ".env", "mode": "dev"}
        
        def select(message: Dict[str, str]) -> bool:
            return False

        show(f"{application_name:s} 1")        
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 2")   
            # sample = Actions.create_sample(application, select)
            show(f"{application_name:s} 3")
        
        show(f"{application_name:s} 4")
    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
 
