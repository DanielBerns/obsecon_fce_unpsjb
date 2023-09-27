from collections import defaultdict
from dataclasses import dataclass
import logging
from typing import Tuple, List, Protocol, Dict, Generator, DefaultDict
from math import log

from context import components
from components.helpers import classname

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

def sp(width: int, data: str) -> str:
    sp_width = width - len(data) - 1
    return ' '*sp_width + '$' + data if sp_width > 0 else '$' + data


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
        self.per_place[place] = point_of_sale
        self.per_identifier[point_of_sale.identifier] = point_of_sale

    def values(self) -> PointOfSale:
        for identifier, point_of_sale in self.per_identifier.items():
            yield point_of_sale


class ArticleWithPrices:
    def __init__(self, 
                 article: Article,
                 prices: List[Tuple[str, int]]) -> None:
        self._article = article
        if len(prices) == 0:
            logging.debug(f"{classname(self):s}.__init__ 1")
            logging.debug(f"{article.code:s} len(prices) == 0")
            raise ModelsException(f"{classname(self):s}.__init__ 1")
        ordered_prices = sorted(prices, key = lambda x: x[1])
        try:
            float_prices = [float(price) / 100 for point_of_sale, price in ordered_prices]
        except ValueError:
            logging.error(f"ERROR: bad prices {self.place:s}:{self.article.code:s}")
            raise ModelsException(f"{classname(self):s}.__init__ 2")            
        else:
            prices_min, prices_max = float_prices[0], float_prices[-1]
            log_float_prices = [log(pp, 10) for pp in float_prices]                        
            log_prices_geomean = sum(log_float_prices) / len(log_float_prices)
            prices_geomean = 10**log_prices_geomean        
            self._prices_stats = tuple((f"{pp:>.2f}" for pp in (prices_min, prices_geomean, prices_max)))
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
    def formatted_prices(self) -> List[Tuple[str, int]]:
        return self._formatted_prices
    
    @property
    def prices_stats(self) -> Tuple[str, str, str]:
        return self._prices_stats

    def label(self) -> str:
        return f"{self.article.code:s}: {self.article.brand:s} - {self.article.name:s}"
    
    def prices_min(self, width: int) -> str:
        return f"{sp(width, self.prices_stats[0]):s}"

    def prices_geomean(self, width: int) -> str:
        return f"{sp(width, self.prices_stats[1]):s}"

    def prices_max(self, width: int) -> str:
        return f"{sp(width, self.prices_stats[2]):s}"


class ArticleWithPricesTable:
    def __init__(self, 
                 timestamp: str, 
                 place: str,
                 some_keys: Optional[List] = None) -> None:
        self._timestamp = timestamp        
        self._place = place
        self._some_keys = some_keys
        self._article_with_prices: Dict[str, ArticleWithPrices] = dict()

    @property
    def timestamp(self) -> str:
        return self._timestamp
                                 
    @property
    def place(self) -> str:
        return self._place

    @property   
    def some_keys(self) -> List[str]:
        return self._some_keys
    
    @some_keys.setter
    def some_keys(self, value: List[str]) -> None:
        self._some_keys = value

    @property
    def article_with_prices(self) -> Dict[str, ArticleWithPrices]:
        return self._article_with_prices
    
    def add(self, 
            article: Article, 
            prices: List[PointOfSaleAndPrice]) -> None:
        self.article_with_prices[article.code] = ArticleWithPrices(article, prices)

    def values(self) -> Generator[ArticleWithPrices, None, None]:
        if self.some_keys:
            for code in self.some_keys:
                yield self.article_with_prices[code]
        else:       
            for code, article_with_prices in self.article_with_prices.items():
                yield article_with_prices

    def all_the_values(self) -> Generator[ArticleWithPrices, None, None]:
        for code, article_with_prices in self.article_with_prices.items():
            yield article_with_prices

    def some_values(self) -> Generator[ArticleWithPrices, None, None]:
        if self.some_keys:
            for code in self.some_keys:
                yield self.article_with_prices[code]


class PricesPerPointOfSaleTable:
    def __init__(self) -> None:    
        self._point_of_sale_and_price: DefaultDict[str, List[PointOfSaleAndPrice]] = defaultdict(list)

    @property
    def point_of_sale_and_price(self) -> DefaultDict[str, List[PointOfSaleAndPrice]]:
        return self._point_of_sale_and_price

    def add(self, 
            article_code: str, 
            point_of_sale: PointOfSale, price: int
            ) -> None:
        self._point_of_sale_and_price[article_code] = (point_of_sale, price)

    def values(self) -> Tuple[PointOfSale, int]:
        for article_code, (point_of_sale, price) in self.point_of_sale_and_price.items():
            yield (point_of_sale, price)

    
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
        
