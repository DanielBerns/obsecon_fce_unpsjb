from contextlib import contextmanager
import json
import logging
from pathlib import Path

from typing import Dict, Optional, Generator, Any, List

from web_scraper import WebScraper
from context import components
from components.core import EventsSource, EventsDocument
from components.helpers import get_container

import pdb

class PointsOfSaleSource(EventsSource):
    def __init__(self, 
                 identifier: str, 
                 web_scraper: WebScraper):
        super().__init__(identifier)
        self._web_scraper = web_scraper
        
    @property
    def web_scraper(self) -> WebScraper:
        return self._web_scraper
    
    def events(self) -> Generator[Dict[Any, Any], None, None]:
        for event in self.web_scraper.points_of_sale():
            yield event
        

class SelectedPointsOfSaleSource(EventsSource):
    def __init__(self, 
                 identifier: str, 
                 selectors: List[Dict[str, str]]
                 ):
        super().__init__(identifier)
        self._selectors = selectors
        self._all_the_points_of_sale: Optional[EventsDocument] = None

    @property        
    def selectors(self) -> List[Dict[str, str]]:
        return self._selectors
    
    @property        
    def all_the_points_of_sale(self) -> Optional[EventsDocument]:
        return self._all_the_points_of_sale
    
    @all_the_points_of_sale.setter
    def all_the_points_of_sale(self, value: EventsDocument) -> None:
        self._all_the_points_of_sale = value

    def events(self) -> Dict[Any, Any]:
        for ee in self.all_the_points_of_sale.events():
            event = EventsDocument.lower_values(ee)
            itera = (event['provincia'] == ss['provincia'] and event['localidad'] == ss['localidad'] for ss in self.selectors)
            if any(itera):
                processed_event = {
                    'identifier': event['id'],
                    'provincia': event['provincia'],
                    'localidad': event['localidad'],
                    'direccion': event['direccion'],
                    'bandera'  : event['banderaDescripcion'],
                    'comercio' : event['comercioRazonSocial'],
                    'sucursal' : event['sucursalNombre'],
                    }
                yield processed_event

  
class ArticlesPerPointOfSaleSource(EventsSource):
    def __init__(self, identifier: str, web_scraper: WebScraper) -> None:
        super().__init__(identifier)
        self._web_scraper: WebScraper = web_scraper
        self._points_of_sale: Optional[EventsSource] = None 
        
    @property
    def web_scraper(self) -> WebScraper:
        return self._web_scraper

    @property
    def points_of_sale(self) -> EventsSource:
        return self._points_of_sale
    
    @points_of_sale.setter
    def points_of_sale(self, value: EventsSource) -> None:
        self._points_of_sale = value
    
    def events(self):
        for this_point_of_sale in self.points_of_sale.events():
            for aa in self.web_scraper.articles_per_point_of_sale(this_point_of_sale):
                article = EventsDocument.lower_values(aa)
                processed_article = {
                  'identifier': article['id'],
                  'marca': article['marca'],
                  'nombre': article['nombre'],
                  'presentacion': article['presentacion'],          
                  'precio': article['precio'],
                  'precio_max': article['precioMax'],
                  'precio_min': article['precioMin'],
                  'point_of_sale': article['point_of_sale']        
                }
                yield processed_article


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


class Downloader:
   
    def __init__(self, 
                 web_scraper: WebScraper, 
                 selectors: Dict[str, str]):
        self._web_scraper = web_scraper
        self._points_of_sale_source = PointsOfSaleSource('downloader.points_of_sale', self.web_scraper)
        self._selected_points_of_sale_source = SelectedPointsOfSaleSource('downloader.selected_points_of_sale', selectors)
        self._articles_per_point_of_sale_source = ArticlesPerPointOfSaleSource('downloader.articles_per_point_of_sale', self.web_scraper)

    @property
    def web_scraper(self) -> WebScraper:
        return self._web_scraper
    
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
        
    def stop(self) -> None:
        logging.info("stop")
        
    def write(self, sample_path: Path):
        sample = PreciosClarosSample(sample_path)
        sample.start()
        sample.points_of_sale.update(self.points_of_sale_source)
        self.selected_points_of_sale_source.all_the_points_of_sale = sample.points_of_sale
        sample.selected_points_of_sale.update(self.selected_points_of_sale_source)
        self.articles_per_point_of_sale_source.points_of_sale = sample.selected_points_of_sale
        pdb.set_trace()
        sample.articles_per_point_of_sale.update(self.articles_per_point_of_sale_source)
        sample.stop()

    def test(self, sample_path: Path):
        sample = PreciosClarosSample(sample_path)
        sample.start()
        # sample.points_of_sale.update(self.points_of_sale_source)
        self.selected_points_of_sale_source.all_the_points_of_sale = sample.points_of_sale
        sample.selected_points_of_sale.update(self.selected_points_of_sale_source)
        self.articles_per_point_of_sale_source.points_of_sale = sample.selected_points_of_sale
        sample.articles_per_point_of_sale.update(self.articles_per_point_of_sale_source)
        sample.stop()
