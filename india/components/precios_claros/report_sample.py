from collections import defaultdict, Counter
from pathlib import Path
from typing import DefaultDict, List, Generator, Dict, Tuple
import math
from os import walk
import logging
from dataclasses import dataclass

from components.helpers import get_resource, get_container, i, classname
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import (Article, 
                    PointOfSale, 
                    ArticleWithPricesTable, 
                    PointsOfSaleTable, 
                    PreciosClarosTask)

from components.precios_claros.writers import (WriterWithTargetFormat,
                                               ArticleWithPricesTableHTML,
                                               ArticleWithPricesTableMD)


class ReportSampleError(Exception):
    pass


class PointsOfSaleCollector:
    
    def __init__(self) -> None:
        self._table = PointsOfSaleTable()

    @property
    def table(self) -> PointsOfSaleTable:
        return self._table

    def update(self, event: Dict[str, str]) -> None:
        identifier = event['identifier']
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
    def __init__(self,
                 points_of_sale_table: PointsOfSaleTable
                 ) -> None:
        self._points_of_sale_table: PointsOfSaleTable = points_of_sale_table
        self._articles_counter: Counter = Counter()
        self._articles: Dict[str, Article] = dict()
        self._prices: DefaultDict[str, List[Tuple[PointOfSale, int]]] = defaultdict(list)

    @property
    def points_of_sale_table(self) -> PointsOfSaleTable:
        return self._points_of_sale_table

    @property
    def articles_counter(self) -> Counter:
        return self._articles_counter

    @property
    def articles(self) -> Dict[str, Article]:
        return self._articles

    @property
    def prices(self) -> DefaultDict[str, List[Tuple[PointOfSale, int]]]:
        return self._prices
    
    def update(self, event: Dict[str, str]) -> None:
        article_code = event['identifier']
        brand = (event['marca']).lower()
        name = (event['nombre']).lower()
        package = (event['presentacion']).lower()
        _price = event['precio']
        point_of_sale_identifier = event['point_of_sale']
        
        if article_code.startswith('['):
            if article_code.endswith(']'):
                article_code = article_code[1:-1]
            else:
                raise ReportSampleError(
                   f"{classname(self):s}.update 1")                
        elif article_code.endswith(']'):
            raise ReportSampleError(
                f"{classname(self):s}.update 2")
        else:
            pass
        
        try:
            price = int(float(_price) * 100)
        except ValueError:
            raise ReportSampleError(
                f"{classname(self):s}.update 3")

        try:
            point_of_sale = self.points_of_sale_table.per_identifier[point_of_sale_identifier]
        except KeyError:
            raise ReportSampleError(
                f"{classname(self):s}.update 4")

        self.articles_counter[article_code] += 1
        self.prices[article_code].append((point_of_sale, price))

        if self.articles_counter[article_code] == 1:
            an_article = Article(article_code, brand, name, package)
            self.articles[article_code] = an_article
        else:
            an_article = self.articles[article_code]
            different_events = True
            if brand == an_article.brand:
                if name == an_article.name:
                    if package == an_article.package:
                        different_events = False
            if different_events:
                raise ReportSampleError(
                    f"{classname(self):s}.update 5")


SampleItems = Tuple[str, ArticleWithPricesTable, List[PointOfSale]]


class SampleCollector:
    def __init__(self) -> None:
        self._points_of_sale_collector = PointsOfSaleCollector()        
        self._articles_collector = ArticlesCollector(self.get_points_of_sale_table())
        
    @property
    def articles_collector(self) -> ArticlesCollector:
        return self._articles_collector

    @property
    def points_of_sale_collector(self) -> PointsOfSaleCollector:
        return self._points_of_sale_collector 

    def update(self, sample: PreciosClarosSample):
        for event in sample.selected_points_of_sale.events():
            self.points_of_sale_collector.update(event)        
        for event in sample.articles_per_point_of_sale.events():
            self.articles_collector.update(event)

    def get_points_of_sale_table(self) -> PointsOfSaleTable:
        return self.points_of_sale_collector.table
        
    def get_article_with_prices_table(
        self, 
        home: Path, 
        sample_key: str, 
        place: str
        ) -> ArticleWithPricesTable:
        article_with_prices_table = ArticleWithPricesTable(home, sample_key, place)
        count = 0
        for article_code, prices in self.articles_collector.prices.items():
            count += 1
            # print(f"{article_code:s}: {count:d}")
            try:
                article = self.articles_collector.articles[article_code]
                article_with_prices_table.add(article, prices)
            except KeyError:
                raise ReportSampleError(
                    f"{classname(self):s}.get_article_with_prices_table: "
                    f"bad article_code {article_code:s}"
                    )
        return article_with_prices_table

    def sample_items(self, home: Path, sample_key: str) -> Generator[SampleItems, None, None]:
        logging.debug(f"{classname(self):s}.execute: {sample_key:s} started!")    
        # target_container = get_container(home, sample_key)
        points_of_sale_table = self.get_points_of_sale_table()
        count = 0
        for place, points_of_sale in points_of_sale_table.per_place.items():
            count += 1
            # print(f"{place:s}: {count:d}")
            article_with_prices_table = self.get_article_with_prices_table(home, sample_key, place)
            logging.debug(f"{classname(self):s}.execute: {sample_key:s} at {place:s} started!")                
            yield place, article_with_prices_table, points_of_sale
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
                sample_key: str
                ) -> None:
        target_container = get_container(home, sample_key)
        # print(f"{str(target_container):s}")
        writer = WriterWithTargetFormat(target_container)        
        for place, article_with_prices_table, points_of_sale in self.sample_collector.sample_items(home, sample_key):
            writer.target_format = ArticleWithPricesTableMD()
            writer.execute(place, "todos", article_with_prices_table, points_of_sale)
            for category in self.get_categories(home, "article_with_prices_selectors"):
                writer.target_format = ArticleWithPricesTableHTML()
                writer.execute(place, category, article_with_prices_table, points_of_sale)
