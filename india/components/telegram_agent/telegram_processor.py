from components.core import TreeStore, TreeStoreProcessor
from components.core import TextReaderImageWithTesseractAndPIL
from components.core import TextReader

from pathlib import Path 
import os

class TelegramSampleProcessor:
    def __init__(self, 
                 results_home: Path,
                 text_reader: TextReader):
        self._results_home = results_home
        self._text_reader = text_reader
        # TextReaderImageWithTesseractAndPIL()
        
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
                if filename == "message.txt":
                    print("    ", "message")
                elif filename == "caption.txt":
                    print("    ", "caption")
                elif filename == "photo.jpeg":
                    print("    ", "photo")
                    text = self.text_reader.read_text(Path(root, filename))
                    with open(Path(root, "text").with_suffix(".txt"), "w") as target:
                        target.write(str(text))
                        target.write("\n")
                        

def processor_run(bot_home: Path, results_home: Path) -> None:
    bot = TelegramBot(bot_home)
    store = bot.store
    dataset_processor = TreeStoreProcessor(store)
    sample_processor = TelegramSampleProcessor(
        results_home,
        TextReaderImageWithTesseractAndPIL())
    dataset_processor.execute(sample_processor)

    
    
