from components.core import (TreeStore, 
                             TreeStoreProcessor,
                             TextReader, 
                             TextReaderHTMLWithBS4)

from components.website_agent.website_bot import WebsiteBot

from pathlib import Path 
import os
from typing import Dict, List

class WebsiteSampleProcessor:
    def __init__(self, 
                 results_home: Path, 
                 text_reader: TextReader):
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
   
def processor_run(
    bot_home: Path,
    websites: Dict[str, List[str]],
    results_home: Path,
    text_reader: TextReader
    ) -> None:
    logging.info(f"start run: {str(bot_home):s} -> {str(results_home):s}")
    for identifier, urls in websites.items():
        logging.info(f"  identifier: {identifier:s}")        
        bot = WebsiteBot(bot_home, identifier)
        bot.store.start()
        sample_processor = WebsiteSampleProcessor(results_home, identifier, text_reader)
        dataset_processor = TreeStoreProcessor(store)
        dataset_processor.execute(sample_processor)
        bot.store.stop()
        logging.info(f"  done: {identifier:s}")                
    logging.info(f"done run: {str(bot_home):s} -> {str(results_home):s}")
