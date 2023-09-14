import logging
from typing import Dict, Generator
from components.helpers import classname, i

class HotelScraper:
    def __init__(self, home: Path) -> None:
        self._home: Path = home
        self._cache: Optional[List[Dict[str, str]]] = None
        self._cache_index: Dict[str, Tuple[int, int]] = dict()

    @property    
    def home(self) -> Path:
        return self._home

    @property
    def cache(self) -> Optional[List[Dict[str, str]]]:
        return self._cache

    @cache.setter
    def cache(self, value: List[Dict[str, str]]) -> None:
        self._cache = value

    @property
    def cache_index(self) -> Dict[str, Tuple[int, int]:
        return self._cache_index

    def start(self) -> None:
        logging.info(f"{classname(self):s}.start")
        container = get_container(self.home, 'points_of_sale')
        doc = EventsDocument(container, "info", ".json.csv")
        self.cache = [{str(key): str(value).lower()} for key, value in event.items()] 
        first_event = self.cache[0]
        last_key = first_event['identifier']
        cursor = begin = end = 0
        for event in self.cache[1:]:
            if event['identifier'] == last_key:
                cursor += 1
            else:
                end = cursor
                self.cache_index[last_key] = (begin, end)
                last_key = event['identifier']
                begin = cursor
    
    def stop(self) -> None:
        logging.info(f"{classname(self):s}.stop")

    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f"{classname(self):s}.points_of_sale")        
        container = get_container(self.home, 'points_of_sale')
        doc = EventsDocument(container, "info", ".json.csv")
        for event in docs.events():
            pos = {str(key): str(value).lower()} for key, value in event.items()}
            yield pos 

    def articles_per_point_of_sale(
        self, 
        point_of_sale: Dict[str, str]
        ) -> Generator[Dict[str, str], None, None]:
        logging.info(f"{classname(self):s}.articles_per_point_of_sale")
        identifier = point_of_sale['identifier']
        begin, end = self.cache_index[identifier]
        for event in self.cache[begin, end]:
            appos = {str(key): str(value).lower()} for key, value in event.items()}
            yield appos 
