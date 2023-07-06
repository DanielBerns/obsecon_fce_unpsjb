import logging
import random
from typing import List

from components.config import Config
from components.core import FileSystem, Metadata, JSONDocument
from components.helpers import save_json, get_container, get_resource_identifier
from components.logs import add_stdout_handler


def create_metadata(fs: FileSystem):
    container = get_container(fs.data, "metadata")
    metadata = Metadata(container)
    metadata.start()
    metadata.add_item("download", "20221118", {"stage": "raw"})
    metadata.add_item("download", "20221119", {"stage": "raw"})
    metadata.add_item("download", "20221120", {"stage": "raw"})
    metadata.stop()


def read_metadata(fs: FileSystem):
    container = get_container(fs.data, "metadata")
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


class EventsStore:
    def __init__(self, store: List):
        self._store = store

    @property
    def store(self) -> List:
        return self._store

    def events(self):
        for e in self.store:
            yield e


def create_json_document(fs: FileSystem) -> None:
    container = get_container(fs.data, "json_document")
    document = JSONDocument(container)
    document.start()
    es = EventsStore([create_event() for i in range(10)])
    document.update(es)
    document.stop()


def read_json_document(fs: FileSystem) -> None:
    container = get_container(fs.data, "json_document")
    document = JSONDocument(container)
    document.start()
    print(str(document.store))
    for value in document.events():
        print(value)
        # for k, v in value.items():
        #    print('  ', k, v)
    document.stop()


def main():
    logger = logging.getLogger(__name__)
    add_stdout_handler(logger)
    logger.setLevel(logging.DEBUG)
    logger.info("<cfg>")
    cfg = Config()
    logger.info("</cfg>")
    logger.info("<fs>")
    fs = FileSystem(cfg.home)
    logger.info("</fs>")
    logger.info("<create_metadata>")
    create_metadata(fs)
    logger.info("</create_metadata>")
    logger.info("<read_metadata>")
    read_metadata(fs)
    logger.info("</read_metadata>")
    logger.info("<create_json_document>")
    create_json_document(fs)
    logger.info("</create_json_document>")
    logger.info("<read_json_document>")
    read_json_document(fs)
    logger.info("</read_json_document>")


if __name__ == "__main__":
    main()
