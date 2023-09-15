from contextlib import contextmanager
import json
import logging
from pathlib import Path

from typing import Dict, Optional, Generator, Any, List

from pc_scraper import PreciosClarosScraper
from context import components
from components.core import EventsSource, EventsDocument
from components.helpers import get_container, i


class PointsOfSale:
    def __init__(self, scraper: PreciosClarosScraper):
        self._scraper: PreciosClarosScraper = scraper
        
    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper
    
    def events(self) -> Generator[Dict[Any, Any], None, None]:
        for number, event in enumerate(self.scraper.points_of_sale()):
            if number % 100 == 1:
                print(f"event #{number:d}")
            yield event




class ArticlesPerPointOfSale:
    def __init__(self, scraper: PreciosClarosScraper) -> None:
        self._scraper: PreciosClarosScraper = scraper

    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper

    def events(self, point_of_sale: Dict[any, any]) -> Generator[Dict[any, any], None, None]:
        for number, article in enumerate(self.scraper.articles_per_point_of_sale(point_of_sale)):        
            if number % 100 == 1:
                print(f'{i(1):s}event #{number:d}')
            yield article


class SelectedPointsOfSaleSource(SelectedEventsSource):
    def __init__(self, 
                 selectors: List[Dict[str, str]]
                 ) -> None:
        super().__init__()
        self._selectors = selectors

    @property        
    def selectors(self) -> List[Dict[str, str]]:
        return self._selectors

    def select_event(self, event: Dict[Any, Any]) -> bool:
        itera = (event['provincia'] == ss['provincia'] and \
                 event['localidad'] == ss['localidad'] \
                     for ss in self.selectors)
        return any(itera)


class SelectedPointsOfSaleReader:
    def __init__(self) -> None:
        self._scraper: PreciosClarosScraper = scraper
        
    @property
    def scraper(self) -> PreciosClarosScraper:
        return self._scraper
    
    def events(self) -> Generator[Dict[Any, Any], None, None]:
        for number, event in enumerate(self.scraper.selected_points_of_sale()):
            if number % 100 == 1:
                print(f"event #{number:d}")
            yield event


class ProcessedPointsOfSaleSource(ProcessedEventsSource):
    def __init__(self):
        super().__init__()

    def process_event(self, x: Dict[Any, Any]) -> Dict[Any, Any]:
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
    def __init__(self, 
                 points_of_sale: PointsOfSale,
                 articles_per_point_of_sale: ArticlesPerPointOfSale) -> None:
        super().__init__()
        self.events_source = points_of_sale
        self.events_processor = articles_per_point_of_sale

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


class Sampler:
   
    @staticmethod
    def create_sample_from_web(selectors: Dict[str, str]) -> Sampler:
        scraper = WebScraper()  
        pos = PointsOfSaleSource(scraper)        
        spos = SelectedPointsOfSaleSelector(selectors)
        spos.events_source = pos
        appos = ArticlesPerPointOfSaleDriver(self.scraper)
        appos.event_source = appos
        return Sampler(scraper, pos, spos, appos)
    
    @staticmethod
    def create_hotel_sampler() -> Sampler:
        scraper = HotelScraper()
        pos = PointsOfSaleSource(scraper)        
        spos = SelectedPointsOfSaleReader(scraper)
        appos = ArticlesPerPointOfSaleDriver(scraper)
        return Sampler(scraper, pos, spos, appos)


    def __init__(self, 
                 points_of_sale_source: EventsSource,
                 selected_points_of_sale_source: EventsSource,
                 articles_per_point_of_sale_source: EventsSource
                 ) -> None:
        self._points_of_sale_source = points_of_sale_source
        self._selected_points_of_sale_source = selected_points_of_sale_source
        self._articles_per_point_of_sale_source = articles_per_point_of_sale_source

    @property
    def points_of_sale_source(self) -> PointsOfSaleSource:
        return self._points_of_sale_source
    
    @property
    def selected_points_of_sale_source(self) -> SelectedPointsOfSaleSource:
        return self._selected_points_of_sale_source
    
    @property
    def articles_per_point_of_sale_source(self) -> ArticlesPerPointOfSaleSource:
        return self._articles_per_point_of_sale_source
    
    def start(self) -> None:
        logging.info("start")
        # self.scraper.start()
        
    def stop(self) -> None:
        # self.scraper.stop()        
        logging.info("stop")
        
    def write(self, sample_path: Path):
        sample = PreciosClarosSample(sample_path)
        sample.start()
        sample.points_of_sale.update(self.points_of_sale_source)
        sample.selected_points_of_sale.update(self.selected_points_of_sale_source)
        sample.articles_per_point_of_sale.update(self.articles_per_point_of_sale_source)
        sample.stop()

 
