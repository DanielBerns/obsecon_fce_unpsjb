from contextlib import contextmanager
import logging
from pathlib import Path
from typing import Dict, Generator, Optional, List, Tuple

from components.helpers import classname, i, get_container, get_timestamp
from components.core import EventsDocument

class LocalScraperError(Exception):
    pass

class LocalScraper:
    def __init__(self, home: Path) -> None:
        self._home: Path = home
        self._cache_index: Dict[str, Tuple[int, int]] = dict()
        container = get_container(self.home, 'articles_per_point_of_sale')
        doc = EventsDocument(container, "info", ".json.csv")
        self._cache: List[Dict[str, str]] = [
            {str(key): str(value).lower() for key, value in event.items()} \
            for event in doc.events()]
        if self.cache:
            first_event = self.cache[0]
            current_key = first_event['point_of_sale']
            cursor = begin = end = 0
            for event in self.cache[1:]:
                if event['point_of_sale'] != current_key:
                    cursor += 1
                    end = cursor
                    self.cache_index[current_key] = (begin, end)
                    print(current_key, begin, end)
                    current_key = event['point_of_sale']
                    begin = end = cursor
                else:
                    cursor += 1
            end = cursor + 1
            self.cache_index[current_key] = (begin, end)
            print(current_key, begin, end)
        else:
            raise LocalScraperError(f"{classname(self):s}.__init__: no cache.")
        
    @property    
    def home(self) -> Path:
        return self._home

    @property
    def run_identifier(self) -> str:
        return self.home.parts[-1]

    @property
    def cache(self) -> List[Dict[str, str]]:
        return self._cache

    @cache.setter
    def cache(self, value: List[Dict[str, str]]) -> None:
        self._cache = value

    @property
    def cache_index(self) -> Dict[str, Tuple[int, int]]:
        return self._cache_index

    def start(self) -> None:
        logging.info(f"{classname(self):s}.start")
    
    def stop(self) -> None:
        logging.info(f"{classname(self):s}.stop")

    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f"{classname(self):s}.points_of_sale")        
        container = get_container(self.home, 'points_of_sale')
        doc = EventsDocument(container, "info", ".json.csv")
        for event in doc.events():
            pos = {str(key): str(value).lower() for key, value in event.items()}
            yield pos 
            
    def selected_points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f"{classname(self):s}.selected_points_of_sale")        
        container = get_container(self.home, 'selected_points_of_sale')
        doc = EventsDocument(container, "info", ".json.csv")
        for event in doc.events():
            pos = {str(key): str(value).lower() for key, value in event.items()}
            yield pos         

    def articles_per_point_of_sale(
        self, 
        point_of_sale: Dict[str, str]
        ) -> Generator[Dict[str, str], None, None]:
        logging.info(f"{classname(self):s}.articles_per_point_of_sale")
        identifier = point_of_sale['identifier']
        begin, end = self.cache_index[identifier]
        for event in self.cache[begin: end]:
            appos = {str(key): str(value).lower() for key, value in event.items()}
            yield appos 
            
            
@contextmanager
def create_local_scraper():
    resource = LocalScraper()
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(message)
    finally:
        resource.stop()
