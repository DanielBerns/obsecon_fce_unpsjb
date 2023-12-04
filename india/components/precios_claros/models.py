from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
import logging
from typing import Tuple, List, Protocol, Dict, Generator, DefaultDict, Optional
from math import log

from components.helpers import classname, get_container, get_resource


@dataclass
class PointOfSale:
    identifier: str
    name: str
    province: str
    city: str
    address: str

@dataclass
class Article:
    code: str
    brand: str
    name: str
    package: str

PointOfSaleAndPrice = Tuple[PointOfSale, int]


class ModelsException(Exception):
    pass


class PointsOfSaleTable:
    def __init__(self) -> None:    
        self._per_place: DefaultDict[str, List[PointOfSale]] = defaultdict(list)
        self._per_identifier: Dict[str, PointOfSale] = dict()                                      

    @property
    def per_place(self) -> DefaultDict[str, List[PointOfSale]]:
        return self._per_place
                                 
    @property
    def per_identifier(self) -> Dict[str, PointOfSale]:
        return self._per_identifier
    
    def add(self, place: str, point_of_sale: PointOfSale) -> None:
        self.per_place[place].append(point_of_sale)
        self.per_identifier[point_of_sale.identifier] = point_of_sale

    def values(self) -> Generator[PointOfSale, None, None]:
        for identifier, point_of_sale in self.per_identifier.items():
            yield point_of_sale


class ArticleWithPrices:
    def __init__(self, 
                 article: Article,
                 prices: List[Tuple[PointOfSale, int]]) -> None:
        self._article = article
        if len(prices) == 0:
            logging.debug(f"{classname(self):s}.__init__ 1")
            logging.debug(f"{article.code:s} len(prices) == 0")
            raise ModelsException(f"{classname(self):s}.__init__ 1")
        ordered_prices = sorted(prices, key = lambda x: x[1])
        try:
            float_prices = [float(price) / 100 for point_of_sale, price in ordered_prices]
        except ValueError:
            logging.error(f"ERROR: bad prices {self.article.code:s}")
            raise ModelsException(f"{classname(self):s}.__init__ 2")            
        else:
            prices_min, prices_max = float_prices[0], float_prices[-1]
            log_float_prices = [log(pp, 10) for pp in float_prices]                        
            log_prices_geomean = sum(log_float_prices) / len(log_float_prices)
            prices_geomean = 10**log_prices_geomean        
            self._prices_stats = (f"{prices_min:>.2f}", 
                                  f"{prices_geomean:>.2f}", 
                                  f"{prices_max:>.2f}")
            self._formatted_prices = [(a, b, c) for a, b, c in zip(
                                              (pos for pos, pp in ordered_prices),
                                              (pp for pos, pp in ordered_prices),
                                              (f"{pp:>.2f}" for pp in float_prices)
                                              )
            ]

    @property
    def article(self) -> Article:
        return self._article
    
    @property
    def formatted_prices(self) -> List[Tuple[PointOfSale, int, str]]:
        return self._formatted_prices
    
    @property
    def prices_stats(self) -> Tuple[str, str, str]:
        return self._prices_stats

    def label(self) -> str:
        v0 = f"{self.article.code:s}: {self.article.brand:s}: {self.article.name:s}"
        return v0 

    def prices_min(self) -> str:
        return f"{self.prices_stats[0]:s}"

    def prices_geomean(self) -> str:
        return f"{self.prices_stats[1]:s}"

    def prices_max(self) -> str:
        return f"{self.prices_stats[2]:s}"
        
    def prices_range(self) -> str:
        if self.prices_stats[0] == self.prices_stats[2]:
            variable = f"precio uniforme de {self.prices_min():s}"
        else:
            variable = f"precio mínimo de {self.prices_min():s} y un precio máximo de {self.prices_max():s}"
        return "Para este artículo se observó un " + variable
        


class ArticleWithPricesTable:

    def __init__(self, 
                 home: Path,
                 timestamp: str, 
                 place: str) -> None:
        self._home: Path = home
        self._timestamp: str = timestamp        
        self._place: str = place
        self._selectors: Optional[List[str]] = None
        self._article_with_prices: Dict[str, ArticleWithPrices] = dict()
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def timestamp(self) -> str:
        return self._timestamp
                                 
    @property
    def place(self) -> str:
        return self._place

    @property   
    def selectors(self) -> Optional[List[str]]:
        return self._selectors

    @selectors.setter
    def selectors(self, value: List[str]) -> None:
        self._selectors = value if value else None
        
    def load_selectors(self, category: str) -> None:
        resource = get_resource(
            Path(self.home, "article_with_prices_selectors", category), 
            "selectors", ".txt")
        if resource.exists():
            with open(resource, "r") as origin:
                self.selectors = [line[:-1] for line in origin]
        else:
            pass

    @property
    def article_with_prices(self) -> Dict[str, ArticleWithPrices]:
        return self._article_with_prices
    
    def add(self, 
            article: Article, 
            prices: List[PointOfSaleAndPrice]) -> None:
        self.article_with_prices[article.code] = ArticleWithPrices(article, prices)

    def values(self) -> Generator[ArticleWithPrices, None, None]:
        if self.selectors:
            method = self.selectors[0]
            if method == "article_code":
                for code in self.selectors[1:]:
                    try:
                        yield self.article_with_prices[code]
                    except KeyError:
                        continue
            elif method == "prefix":
                for a_prefix in self.selectors[1:]:
                    for code, article_with_prices in self.article_with_prices.items():
                        if article_with_prices.article.name.startswith(a_prefix):
                            yield article_with_prices                
            else:
                logging.warning(f"{classname(self):s}.values: bad method {method:s}")
        else:       
            for code, article_with_prices in self.article_with_prices.items():
                yield article_with_prices

    def all_of_them(self) -> Generator[ArticleWithPrices, None, None]:
        for code, article_with_prices in self.article_with_prices.items():
            yield article_with_prices
        

class PricesPerPointOfSaleTable:
    def __init__(self) -> None:    
        self._point_of_sale_and_price: DefaultDict[str, List[PointOfSaleAndPrice]] = defaultdict(list)

    @property
    def point_of_sale_and_price(self) -> DefaultDict[str, List[PointOfSaleAndPrice]]:
        return self._point_of_sale_and_price

    def add(self, 
            article_code: str, 
            point_of_sale: PointOfSale, 
            price: int
            ) -> None:
        self.point_of_sale_and_price[article_code].append((point_of_sale, price))

    def values(self) -> Generator[List[Tuple[PointOfSale, int]], None, None]:
        for article_code, point_of_sale_with_price in self.point_of_sale_and_price.items():
            yield point_of_sale_with_price

    
SampleTables = Tuple[str, ArticleWithPricesTable, PointsOfSaleTable]

            
class PreciosClarosTaskException(Exception):
    pass


class PreciosClarosTask(Protocol):

    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass
    
    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: PointsOfSaleTable) -> None:
        pass
        
