from components.core import (TreeStore, 
                             TreeStoreProcessor,
                             TextReader, 
                             TextReaderHTMLWithBS4)

from pathlib import Path 
import os

class WebsiteSampleProcessor:
    def __init__(self, results_home: Path, text_reader: TextReader):
        self._results_home = results_home
        self._text_reader = text_reader
        
    @property
    def results_home(self) -> Path:
        return self._results_home
    
    @property
    def text_reader(self) -> TextReader:
        return self._text_reader
    
    def execute(self, sample: Path) -> None:
        print(str(sample))
        for root, dirs, files in os.walk(sample, topdown=False):
            for filename in files:
                print(root, '->', filename)
                if filename == "attributes.json":
                    print("    ", "attributes.json")
                elif filename == "page.html":
                    print("    ", "page.html")
                    text = self.text_reader.read_text(Path(root, filename))
                    with open(Path(root, "text").with_suffix(".txt"), "w") as target:
                        target.write(str(text))
                        target.write("\n")
                elif filename == "text.txt":
                    print("    ", "text.txt")
                        

def processor_start(
    bot_home: Path
    ) -> None:
    store = TreeStore(bot_home, 'messages')
    store.start()
    return TreeStoreProcessor(store)

def processor_run(results_home: Path, 
                  text_reader: TextReader,
                  dataset_processor: TreeStoreProcessor
                  ) -> None:
    sample_processor = WebsiteSampleProcessor(results_home, text_reader)
    dataset_processor.execute(sample_processor)
    
