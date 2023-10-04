from collections import defaultdict, Counter
from pathlib import Path
from typing import DefaultDict, List, Generator, Dict, Tuple
import math
from os import walk
import logging
from dataclasses import dataclass

from components.helpers import get_resource, get_container, i, classname
from sampler import PreciosClarosSample
from models import (Article, 
                    PointOfSale, 
                    ArticleWithPricesTable, 
                    PointsOfSaleTable, 
                    PreciosClarosTask)

from writers import ArticleWithPricesTableTargetFormat

import pdb

class ReportSamplerException(Exception):
    pass


class PointsOfSaleCollector:
    
    def __init__(self) -> None:
        self._table = PointsOfSaleTable()

    @property
    def table(self) -> PointsOfSaleTable:
        return self._table

    def update(self, event: Dict[str, str]) -> None:
        identifier = event['identifier']
        # name = f"{event['bandera']:s}:{event['comercio']:s}:{event['sucursal']:s}"
        name = f"{event['bandera']:s}"         
        province = event['provincia']
        city = event['localidad']
        address = event['direccion']

        place = f"{province:s}:{city:s}".lower()

        point_of_sale = PointOfSale(
            identifier, 
            name.lower(), 
            province.lower(), 
            city.lower(), 
            address.lower())

        self.table.add(place, point_of_sale)


class ArticlesCollector:
    def __init__(self) -> None:
        self._articles_counter = Counter()
        self._articles: Dict[str, Article] = dict()
        self._prices: DefaultDict[str, List[Tuple[str, str, int]]] = defaultdict(list)

    @property
    def articles_counter(self) -> Counter:
        return self._articles_counter

    @property
    def articles(self) -> Dict[str, Article]:
        return self._articles

    @property
    def prices(self) -> DefaultDict[str, List[Tuple[str, str, int]]]:
        return self._prices
    
    def update(self, event: Dict[str, str]) -> None:
        article_code = event['identifier']
        brand = (event['marca']).lower()
        name = (event['nombre']).lower()
        package = (event['presentacion']).lower()
        _price = event['precio']
        point_of_sale = event['point_of_sale']
        
        if article_code.startswith('['):
            if article_code.endswith(']'):
                article_code = article_code[1:-1]
            else:
                self.errors.append(event)
        elif article_code.endswith(']'):
            self.errors.append(event)
            raise ReportSamplerException(
                f"{classname(self):s}.update 1")
        else:
            pass
        
        try:
            price = int(float(_price) * 100)
        except ValueError:
            price = 0
            self.errors.append(event)
            raise ReportSamplerException(
                f"{classname(self):s}.update 2")
        else:
            self.articles_counter[article_code] += 1
            if self.articles_counter[article_code] == 1:
                an_article = Article(article_code, brand, name, package)
                self.articles[article_code] = an_article
                self.prices[article_code].append((point_of_sale, price))            
            else:
                an_article = self.articles[article_code]
                different_events = True
                if brand == an_article.brand:
                    if name == an_article.name:
                        if package == an_article.package:
                            different_events = False
                if different_events:
                    raise ReportSamplerException(
                        f"{classname(self):s}.update 3")


SampleTables = Tuple[str, ArticleWithPricesTable, PointsOfSaleTable]


class SampleCollector:
    def __init__(self) -> None:
        self._articles_collector = ArticlesCollector()
        self._points_of_sale_collector = PointsOfSaleCollector()
        
    @property
    def articles_collector(self) -> ArticlesCollector:
        return self._articles_collector

    @property
    def points_of_sale_collector(self) -> PointsOfSaleCollector:
        return self._points_of_sale_collector 

    def update(self, sample: PreciosClarosSample):
        for event in sample.articles_per_point_of_sale.events():
            self.articles_collector.update(event)

        for event in sample.selected_points_of_sale.events():
            self.points_of_sale_collector.update(event)

    def get_points_of_sale_table(self) -> PointsOfSaleTable:
        return self.points_of_sale_collector.table
        
    def get_article_with_prices_table(self, 
                                      home: Path, 
                                      sample_key: str, 
                                      place: str) -> ArticleWithPricesTable:
        article_with_prices = ArticleWithPricesTable(home, sample_key, place)
        for article_code, prices in self.articles_collector.prices.items():
            article = self.articles_collector.articles[article_code]
            article_with_prices.add(article, prices)
        return article_with_prices

    def execute(self, home: Path, sample_key: str) -> Generator[SampleTables, None, None]:
        logging.debug(f"{classname(self):s}.execute: {sample_key:s} started!")    
        target_container = get_container(home, sample_key)
        points_of_sale = self.get_points_of_sale_table()
        for place, points_of_sale in points_of_sale.per_place.items():
            article_with_prices = self.get_article_with_prices_table(home, sample_key, place)
            logging.debug(f"{classname(self):s}.execute: {sample_key:s} at {place:s} started!")                
            yield place, article_with_prices, points_of_sale
            logging.debug(f"{classname(self):s}.execute: {sample_key:s} at {place:s} done!")
        logging.debug(f"{classname(self):s}.execute: {sample_key:s} done!")        



class FullReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector,
                 sample: PreciosClarosSample) -> None:
        self._sample_collector = sample_collector
        self.sample_collector.update(sample)
           
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def get_categories(self, home: Path, identifier: str) -> Generator[str, None, None]:
        container = get_container(home, identifier)
        for root, dirs, files in walk(container):
            for category in dirs:
                yield category
                
    def execute(self,
                home: Path, 
                sample_key: str,
                create_target: Generator[PreciosClarosTask, None, None]) -> None:
        target_container = get_container(home, sample_key)
        for place, article_with_prices, points_of_sale in self.sample_collector.execute(home, sample_key):
            for category in self.get_categories(home, "article_with_prices_selectors"):
                with create_target(target_container) as target:
                    target.target_format = ArticleWithPricesTableTargetFormat()
                    target.execute(place, category, article_with_prices, points_of_sale)
