from components.core import TreeStore, TreeStoreProcessor
from components.core import TextReaderTesseractPIL
from components.core import TextReader

from pathlib import Path 
import os

class TelegramSampleProcessor:
    def __init__(self, results_home: Path):
        self._results_home = results_home
        self._text_reader = TextReaderTesseractPIL()
        
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
                    print(str(text))

def processor_run(telegram_home: Path, results_home: Path) -> None:
    store = TreeStore(telegram_home, 'messages')
    dataset_processor = TreeStoreProcessor(store)
    sample_processor = TelegramSampleProcessor(results_home)
    dataset_processor.execute(sample_processor)

    
    
