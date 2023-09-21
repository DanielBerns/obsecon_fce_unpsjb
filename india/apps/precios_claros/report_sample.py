from collections import defaultdict, Counter
from pathlib import Path
from typing import DefaultDict, List, Generator, Dict, Tuple
import math
import logging
from dataclasses import dataclass

from components.helpers import get_resource, get_container, i
from sampler import PreciosClarosSample

import pdb

@dataclass
class PointOfSale:
    identifier: str
    name: str
    province: str
    city: str
    address: str


class PointsOfSalePerPlace:
    def __init__(self):
        self._table = defaultdict(list)
        self._errors = list()
        
    @property
    def table(self) -> DefaultDict[str, List[PointOfSale]]:
        return self._table

    @property
    def errors(self) -> List[Dict[str, str]]:
        return self._errors

    def update(self, event: Dict[str, str]) -> None:
        identifier = event['identifier']
        name = f"{event['bandera']:s}:{event['comercio']:s}:{event['sucursal']:s}" 
        province = event['provincia']
        city = event['localidad']
        address = event['direccion']

        place = f"{province:s}:{city:s}".lower()
        
        self.table[place].append(
            PointOfSale(identifier, 
                        name.lower(), 
                        province.lower(), 
                        city.lower(), 
                        address.lower()))


@dataclass
class Article:
    brand: str
    name: str
    package: str

            
class ArticlesPerPointOfSale:
    def __init__(self):
        self._table = defaultdict(list)
        self._errors = list()
        self._articles_count = Counter()
        self._articles_per_code = dict()
        
    @property
    def table(self) -> DefaultDict[str, List[Article]]:
        return self._table

    @property
    def errors(self) -> List[Dict[str, str]]:
        return self._errors

    @property
    def articles_count(self) -> Counter:
        return self._articles_count

    @property
    def articles_per_code(self) -> Dict[str, Article]:
        return self._articles_per_code
    
    def update(self, event: Dict[str, str]) -> None:
        code = event['identifier']
        brand = (event['marca']).lower()
        name = (event['nombre']).lower()
        package = (event['presentacion']).lower()
        _price = event['precio']
        point_of_sale = event['point_of_sale']
        
        if code.startswith('['):
            if code.endswith(']'):
                code = code[1:-1]
            else:
                self.errors.append(event)
        elif code.endswith(']'):
            self.errors.append(event)
        
        try:
            price = int(float(_price) * 100)
        except ValueError:
            price = 0
            self.errors.append(event)


        self.articles_count[code] += 1
        if self.articles_count[code] == 1:
            an_article = Article(brand, name, package)
            self.articles_per_code[code] = an_article
        else:
            an_article = self.articles_per_code[code]
            different_events = True
            if brand == an_article.brand:
                if name == an_article.name:
                    if package == an_article.package:
                        different_events = False
            if different_events:
                self.errors.append(event)
        self.table[point_of_sale].append((code, price))

        
class SampleCollector:
    def __init__(self) -> None:
        self._articles_per_point_of_sale = ArticlesPerPointOfSale()
        self._points_of_sale_per_place = PointsOfSalePerPlace()
        
    @property
    def articles_per_point_of_sale(self) -> ArticlesPerPointOfSale:
        return self._articles_per_point_of_sale

    @property
    def points_of_sale_per_place(self) -> PointsOfSalePerPlace:
        return self._points_of_sale_per_place 

    def update(self, sample: PreciosClarosSample):
        for event in sample.articles_per_point_of_sale.events():
            self.articles_per_point_of_sale.update(event)

        for event in sample.selected_points_of_sale.events():
            self.points_of_sale_per_place.update(event)
    
    def get_places_with_point_of_sale_and_price_per_code(self) -> \
        Generator[Tuple[str, Dict[str, Tuple[str, int]]], None, None]:
        for place, points_of_sale in self.points_of_sale_per_place.table.items():
            point_of_sale_and_price_per_code = defaultdict(list)
            for a_point_of_sale in points_of_sale:
                for (code, price) in self.articles_per_point_of_sale.table[a_point_of_sale.identifier]:
                    point_of_sale_and_price_per_code[code].append(
                            (a_point_of_sale, price)
                    )
            yield place, point_of_sale_and_price_per_code


class FullReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector,
                 sample: PreciosClarosSample) -> None:
        self._sample_collector = sample_collector
        self.sample_collector.update(sample)
        
           
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    @property
    def cities(self) -> DefaultDict[str, List[str]]:
        return self._cities

    def write_md(self, home: Path, sample_key: str) -> None:
        sample_container = get_container(home, sample_key)
        for place, prices_per_article in self.sample_collector.get_places_with_point_of_sale_and_price_per_code():
            place_container = get_container(sample_container, place)
            point_of_sale_and_price_per_code_md = get_resource(
                place_container, 'precios', '.md')
            with open(point_of_sale_and_price_per_code_md, 'w') as target:
                target.write(f"# {place:s}\n")
                logging.debug(f"start with {place:s}")
                for article_code, count in self.sample_collector.articles_per_point_of_sale.articles_count.items():
                    prices_list = sorted(prices_per_article[article_code], key = lambda x: x[1])
                    if len(prices_list) == 0:
                        logging.debug(f"{article_code:s} len(prices_list) == 0")
                        continue
                    prices_min, prices_max = prices_list[0][1], prices_list[-1][1]
                    if prices_min == prices_max:
                        prices_min, prices_max, prices_geomean = \
                            prices_min / 100, prices_max / 100, prices_min / 100 
                    else:
                        prices = [math.log(pp[1] / 100, 10) for pp in prices_list]                        
                        prices_min, prices_max, prices_geomean = \
                            prices_min / 100, prices_max / 100, 10**sum(prices)
                    target.write(f"{article_code:s}: ")
                    this_article = self.sample_collector.articles_per_point_of_sale.articles_per_code[article_code]
                    target.write(f"{this_article.brand:s} -")
                    target.write(f" {this_article.name:s} -")
                    target.write(f" {this_article.package:s}\n")
                    for (point_of_sale, price) in prices_list:
                        try:
                            pp = float(price) / 100
                            target.write(f"{i(1):s}{pp:>9.2f} - "
                                         f"{point_of_sale.identifier:>20s} - "
                                         f"{point_of_sale.name} - "
                                         f"{point_of_sale.city} - "
                                         f"{point_of_sale.address}\n" )
                        except ValueError:
                            logging.error(f"ERROR {price:s}")
