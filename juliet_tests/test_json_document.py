# Unittests using the unittest library
class TestJSONDocument(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.doc = JSONDocument(self.temp_dir)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_events(self):
        events = [{"key1": "value1"}, {"key2": "value2"}]
        with open(self.doc.store, "w") as f:
            for event in events:
                json.dump(event, f)
                f.write("\n")
        self.assertEqual(list(self.doc.events()), events)

    # ... more tests for other methods

if __name__ == "__main__":
    unittest.main() 
