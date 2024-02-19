import logging
from pathlib import Path

from context import components
from components.helpers import (get_home, show)
from components.core.application import create_application
from components.core.flatstore import FlatStore


import unittest

APPLICATION: str = "test_flatstore"

class FlatStoreTest(unittest.TestCase):

    def setUp(self):
        print("setup")
        
    def tearDown(self):
        print("teardown")
        
    def test_application(self):
        application_name = APPLICATION
        arguments = {"dotenv": ".env", "mode": "dev"}
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 1")
            storage = application.file_system.storage
            store = FlatStore(storage, "flatstore")
            sample_keys = ['1', '2', '3']
            for key in sample_keys:
                sample_home = store.create_sample_home(key)
            sample_array = [pp for pp in store.iterate()]
            for ss in sample_array:
                print(str(ss))
            assert(len(sample_keys) == len(sample_array))
            show(f"{application_name:s} 2")
        show(f"{application_name:s} 3")
    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
 
