from components.core import TreeStore, TreeStoreProcessor
from components.core import TextReaderTesseractPIL

from pathlib import Path 

class TelegramSampleProcessor:
    def __init__(self, results_home: Path):
        self._results_home = results_home
        self._text_reader = TextReaderTesseractPIL()
        
    def execute(self, sample: Path) -> None:
        print(str(sample))
        for root, dirs, files in os.walk(sample, topdown=False):
            for filename in files:
                print(root, '->', filename)


def processor_run(telegram_home: Path, results_home: Path) -> None:
    store = TreeStore(telegram_home, 'messages')
    dataset_processor = TreeStoreProcessor(store)
    sample_processor = TelegramSampleProcessor(results_home)
    dataset_processor.execute(sample_processor)

    
    
