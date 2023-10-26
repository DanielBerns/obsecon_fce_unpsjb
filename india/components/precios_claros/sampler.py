from contextlib import contextmanager
import json
import logging
from pathlib import Path

from typing import Dict, Optional, Generator, List, Tuple

from components.precios_claros.pc_scraper import PreciosClarosScraper
from components.precios_claros.web_scraper import WebScraper
from components.precios_claros.local_scraper import LocalScraper
from components.core import (EventsOrigin, 
                             EventsDocument, 
                             SelectedEventsOrigin,
                             ProcessedEventsOrigin,
                             CompositeEventsDriver,
                             Events)
from components.helpers import get_container, i, classname

import pdb

class PointsOfSale:
    def __init__(self, scraper: PreciosClarosScraper):
        self._scraper: PreciosClarosScraper = scraper
        
    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper
    
    def events(self) -> Generator[Dict[str, str], None, None]:
        for number, event in enumerate(self.scraper.points_of_sale()):
            if number % 100 == 1:
                print(f"{classname(self):s} event #{number:d}")
            yield event


class ArticlesPerPointOfSale:
    def __init__(self, scraper: PreciosClarosScraper) -> None:
        self._scraper: PreciosClarosScraper = scraper

    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper

    def events(self, point_of_sale: Dict[str, str]) -> Generator[Dict[str, str], None, None]:
        for number, article in enumerate(self.scraper.articles_per_point_of_sale(point_of_sale)):        
            if number % 100 == 1:
                print(f'{i(1):s}{classname(self):s} event #{number:d}')
            yield article


class SelectedPointsOfSaleGenerator(SelectedEventsOrigin):
    def __init__(self, selectors: List[Dict[str, str]]) -> None:
        super().__init__()
        self._selectors = selectors

    @property        
    def selectors(self) -> List[Dict[str, str]]:
        return self._selectors

    def select_event(self, event: Dict[str, str]) -> bool:
        pdb.set_trace()
        itera = (event['provincia'] == ss['provincia'] and \
                 event['localidad'] == ss['localidad'] \
                     for ss in self.selectors)
        return str(itera)


class SelectedPointsOfSaleReader:
    def __init__(self, scraper: PreciosClarosScraper) -> None:
        self._scraper: PreciosClarosScraper = scraper
        
    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper
    
    def events(self) -> Generator[Dict[str, str], None, None]:
        for number, event in enumerate(self.scraper.selected_points_of_sale()):
            if number % 100 == 1:
                print(f"{classname(self):s} event #{number:d}")
            yield Events.lower_values(event)


class ProcessedPointsOfSaleSource(ProcessedEventsOrigin):
    def __init__(self):
        super().__init__()

    def process_event(self, x: Dict[str, str]) -> Dict[str, str]:
        # pdb.set_trace()
        event = Events.lower_values(x)
        processed_event = {
                    'identifier': event['id'],
                    'provincia': event['provincia'],
                    'localidad': event['localidad'],
                    'direccion': event['direccion'],
                    'bandera'  : event['banderaDescripcion'],
                    'comercio' : event['comercioRazonSocial'],
                    'sucursal' : event['sucursalNombre'],
                    }
        return processed_event

            
class ArticlesPerPointOfSaleDriver(CompositeEventsDriver):
    def __init__(self) -> None:
        super().__init__()

    def events(self):
        for article_0 in super().events():
            article_1 = Events.lower_values(article_0)
            article_2 = {
              'identifier': article_1['id'],
              'marca': article_1['marca'],
              'nombre': article_1['nombre'],
              'presentacion': article_1['presentacion'],          
              'precio': article_1['precio'],
              'precio_max': article_1['precioMax'],
              'precio_min': article_1['precioMin'],
              'point_of_sale': article_1['point_of_sale']        
            }
            yield article_2


class PreciosClarosSample:
    def __init__(self, home: Path) -> None:
        self._home = home
        pdb.set_trace()
        self._points_of_sale = EventsDocument(
            get_container(self.home, 'points_of_sale'))
        self._selected_points_of_sale = EventsDocument(
            get_container(self.home, 'selected_points_of_sale'))
        self._articles_per_point_of_sale = EventsDocument(
            get_container(self.home, 'articles_per_point_of_sale'))

    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def points_of_sale(self) -> EventsDocument:
        return self._points_of_sale
    
    @property
    def selected_points_of_sale(self) -> EventsDocument:
        return self._selected_points_of_sale
    
    @property
    def articles_per_point_of_sale(self) -> EventsDocument:
        return self._articles_per_point_of_sale

    def start(self) -> None:
        self.points_of_sale.start()
        self.selected_points_of_sale.start()
        self.articles_per_point_of_sale.start()

    def stop(self) -> None:
        self.points_of_sale.stop()
        self.selected_points_of_sale.stop()
        self.articles_per_point_of_sale.stop()


class PreciosClarosSampleBuilder:

    def __init__(self, 
                 run_identifier: str,
                 points_of_sale_source: EventsOrigin,
                 selected_points_of_sale_source: EventsOrigin,
                 articles_per_point_of_sale_source: EventsOrigin
                 ) -> None:
        self._run_identifier = run_identifier
        self._points_of_sale_source = points_of_sale_source
        self._selected_points_of_sale_source = selected_points_of_sale_source
        self._articles_per_point_of_sale_source = articles_per_point_of_sale_source

    @property
    def run_identifier(self) -> str:
        return self._run_identifier
    
    @property
    def points_of_sale_source(self) -> EventsOrigin:
        return self._points_of_sale_source
    
    @property
    def selected_points_of_sale_source(self) -> EventsOrigin:
        return self._selected_points_of_sale_source
    
    @property
    def articles_per_point_of_sale_source(self) -> EventsOrigin:
        return self._articles_per_point_of_sale_source
    
    def start(self) -> None:
        logging.info("start")
        
    def stop(self) -> None:
        logging.info("stop")
        
    def write(self, sample_path: Path):
        sample = PreciosClarosSample(sample_path)
        sample.start()
        sample.points_of_sale.update(self.points_of_sale_source)
        pdb.set_trace()
        sample.selected_points_of_sale.update(self.selected_points_of_sale_source)
        sample.articles_per_point_of_sale.update(self.articles_per_point_of_sale_source)
        sample.stop()

@contextmanager
def create_sample_with_web_content(selectors: Dict[str, str]) -> PreciosClarosSampleBuilder:
    scraper = WebScraper()  
    pos = PointsOfSale(scraper)   
    ppos = ProcessedPointsOfSaleSource()
    ppos.events_source = pos
    spos = SelectedPointsOfSaleGenerator(selectors)
    spos.events_source = ppos
    appos = ArticlesPerPointOfSale(scraper)
    apposd = ArticlesPerPointOfSaleDriver()
    apposd.events_source = spos
    apposd.events_processor = appos
    resource = PreciosClarosSampleBuilder(scraper.run_identifier, pos, spos, apposd)
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(message)
    finally:
        resource.stop()
    
@contextmanager
def create_sample_with_local_content(home: Path) -> PreciosClarosSampleBuilder:
    scraper = LocalScraper(home.expanduser())
    pos = PointsOfSale(scraper)   
    ppos = ProcessedPointsOfSaleSource()
    ppos.events_source = pos        
    spos = SelectedPointsOfSaleReader(scraper)
    appos = ArticlesPerPointOfSale(scraper)
    apposd = ArticlesPerPointOfSaleDriver()
    apposd.events_source = spos
    apposd.events_processor = appos
    resource = PreciosClarosSampleBuilder(scraper.run_identifier, pos, spos, apposd)
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(message)
    finally:
        resource.stop()
