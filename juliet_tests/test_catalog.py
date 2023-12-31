import unittest
from catalog import Catalog

class TestCatalog(unittest.TestCase):

    def test_create(self):
        catalog: Catalog[str] = Catalog()
        catalog.create("key1", "value1")
        self.assertEqual(catalog.table, {"key1": "value1"})

        with self.assertRaises(CatalogException) as cm:
            catalog.create("key1", "value2")
        self.assertEqual(str(cm.exception), "Entry with key 'key1' already exists.")

    def test_update(self):
        catalog: Catalog[str] = Catalog()
        catalog.create("key1", "value1")
        catalog.update("key1", "new_value")
        self.assertEqual(catalog.table, {"key1": "new_value"})

        with self.assertRaises(CatalogException) as cm:
            catalog.update("key2", "value2")
        self.assertEqual(str(cm.exception), "Entry with key 'key2' not found.")

    def test_delete(self):
        catalog: Catalog[str] = Catalog()
        catalog.create("key1", "value1")
        catalog.delete("key1")
        self.assertEqual(catalog.table, {})

        with self.assertRaises(CatalogException) as cm:
            catalog.delete("key2")
        self.assertEqual(str(cm.exception), "Entry with key 'key2' not found.")

    def test_get(self):
        catalog: Catalog[str] = Catalog()
        catalog.create("key1", "value1")
        self.assertEqual(catalog.get("key1"), "value1")
        self.assertEqual(catalog.get("key2", "default_value"), "default_value")

if __name__ == '__main__':
    unittest.main()
 
