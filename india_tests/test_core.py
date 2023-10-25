import logging
import random
from typing import List
from pathlib import Path

from context import components
from components.core import (FileSystem, 
                             Metadata, 
                             EventsDocument, 
                             RowsDocument, 
                             Config, 
                             TreeStore, 
                             FlatStore)
from components.helpers import get_container, get_resource, get_timestamp, write_text


def create_metadata(fs: FileSystem):
    container = get_container(fs.storage, "metadata")
    metadata = Metadata(container)
    metadata.start()
    metadata.add("download", "20221118", {"stage": "raw"})
    metadata.add("download", "20221119", {"stage": "raw"})
    metadata.add("download", "20221120", {"stage": "raw"})
    metadata.stop()


def read_metadata(fs: FileSystem):
    container = get_container(fs.storage, "metadata")
    metadata = Metadata(container)
    metadata.start()
    print("Original")
    for first_key, second_key, sample in metadata.items():
        print(first_key, " - ", second_key)
        for attribute, value in sample.items():
            print("  ", attribute, " - ", value)
    metadata.events["download"]["20221118"]["process"] = "alpha"
    metadata.events["download"]["20221119"]["process"] = "bravo"
    metadata.events["download"]["20221120"]["process"] = "charlie"
    print("Modified")
    for first_key, second_key, sample in metadata.items():
        print(first_key, " - ", second_key)
        for attribute, value in sample.items():
            print("  ", attribute, " - ", value)


def create_event():
    letters = "abcdefghijklmnopqrstuvwxyz"
    event = {}
    for j in range(5):
        key = "".join([c for c in random.choices(letters, k=10)])
        value = "".join([c for c in random.choices(letters, k=10)])
        event[key] = value
    return event


class EventsOrigin:
    def __init__(self, store: List):
        self._store = store

    @property
    def store(self) -> List:
        return self._store

    def events(self):
        for e in self.store:
            yield e


def create_json_document(fs: FileSystem) -> None:
    container = get_container(fs.storage, "json_document")
    document = EventsDocument(container)
    document.start()
    es = EventsOrigin([create_event() for i in range(10)])
    document.update(es)
    document.stop()


def read_json_document(fs: FileSystem) -> None:
    container = get_container(fs.storage, "json_document")
    document = EventsDocument(container)
    document.start()
    print(str(document.store))
    for value in document.events():
        print(value)
        for k, v in value.items():
           print('  ', k, v)
    document.stop()


def main():
    logging.info("<fs>")
    fs = FileSystem("components", "india", "test")
    logging.info("</fs>")
    logging.info("<create_metadata>")
    create_metadata(fs)
    logging.info("</create_metadata>")
    logging.info("<read_metadata>")
    read_metadata(fs)
    logging.info("</read_metadata>")
    logging.info("<create_json_document>")
    create_json_document(fs)
    logging.info("</create_json_document>")
    logging.info("<read_json_document>")
    read_json_document(fs)
    logging.info("</read_json_document>")
    test_treestore = TreeStore(fs.storage, "treestore")
    alpha = test_treestore.create_sample()
    write_text(get_resource(alpha, 'text', '.txt'), 'alpha 1')
    bravo = test_treestore.create_sample()
    write_text(get_resource(bravo, 'text', '.txt'), 'bravo 2')    
    charlie = test_treestore.create_sample()
    write_text(get_resource(charlie, 'text', '.txt'), 'charlie 3')
    test_flatstore = FlatStore(fs.storage, "flatstore")
    alpha = test_flatstore.create_sample(key='alpha')
    write_text(get_resource(alpha, 'text', '.txt'), 'alpha 1')
    bravo = test_flatstore.create_sample(key='bravo')
    write_text(get_resource(bravo, 'text', '.txt'), 'bravo 2')    
    charlie = test_flatstore.create_sample(key='charlie')
    write_text(get_resource(charlie, 'text', '.txt'), 'charlie 3')    


if __name__ == "__main__":
    main()
