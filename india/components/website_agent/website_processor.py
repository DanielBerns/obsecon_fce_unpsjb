from components.core import (
    TreeStore,
    TreeStoreProcessor,
    FileProcessor
)

from components.website_agent.website_bot import WebsiteBot
from components.helpers import get_container

from pathlib import Path
import os
from typing import Dict, List, Tuple
import logging

class TextFromHTMLSampleTask:
    def __init__(self, 
                 processor_home: Path, 
                 identifier: str, 
                 text_processor: FileProcessor):
        self._results_home = get_container(processor_home, identifier)
        self._text_processor = text_processor

    @property
    def results_home(self) -> Path:
        return self._results_home

    @property
    def text_processor(self) -> FileProcessor:
        return self._text_processor

    def execute(self, sample: Path) -> None:
        print(str(sample))
        for root, dirs, files in os.walk(sample, topdown=False):
            for filename in files:
                print(root, "->", filename)
                if filename == "attributes.json":
                    print("    ", "attributes.json")
                elif filename == "page.html":
                    print("    ", "page.html")
                    self.text_processor.source_identifier = Path(root, filename)
                    self.text_processor.target_identifier = Path(root, "text.txt")
                    self.text_processor.execute()
                elif filename == "text.txt":
                    print("    ", "text.txt")


class TextFromHTMLProcessor(MyProcessor):
    def __init__(self,
                 bot_home: Path,
                 processor_home: Path,
                 text_processor: FileProcessor
                 ) -> None:
        super().__init__(bot_home, processor_home)
        self._text_processor = text_processor
        
    @property
    def text_processor(self) -> FileProcessor:
        return self._text_processor
    
    @text_processor.setter
    def text_processor(self, value: FileProcessor) -> None:
        self._text_processor = value

    def build_sample_task(self, identifier: str) -> SampleTask:
        return TextFromHTMLSampleTask(
            self.processor_home, identifier, self.text_processor
        )
