import logging
import random
from typing import Dict
from pathlib import Path

from context import components
from components.helpers import (get_home, show)
from components.core import (create_application, TreeStore)

import unittest

APPLICATION: str = "test_treestore"

class TreeStoreTestCase(unittest.TestCase):

    def setUp(self):
        print("setup")
        
    def tearDown(self):
        print("teardown")
        
    def test_treestore(self):
        application_name = APPLICATION
        arguments = {"dotenv": ".env", "mode": "dev"}
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 1")
            storage = application.file_system.storage
            store = TreeStore(storage, "treestore")
            sample_top = 3
            for k in range(sample_top):
                sample_home = store.create_sample_home()
            
            sample_array = [pp for pp in store.iterate()]
            for ss in sample_array:
                print(str(ss))
            assert(store.index == len(sample_array))
                
            show(f"{application_name:s} 2")
        show(f"{application_name:s} 3")
    
   

if __name__ == "__main__":
    unittest.main(verbosity=2)
 
