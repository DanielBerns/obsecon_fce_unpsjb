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

    def place(self) -> str:
        return f"{self.province:s}:{self.city:s}"


@dataclass
class Article:
    code: str
    brand: str
    name: str
    package: str


PointOfSaleAndPrice = Tuple[PointOfSale, int]


class ModelsException(Exception):
    def __init__(self, remark: str) -> None:
        logging.error(remark)
        super().__init__(remark)


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

    def add(self, point_of_sale: PointOfSale) -> None:
        self.per_place[point_of_sale.place()].append(point_of_sale)
        self.per_identifier[point_of_sale.identifier] = point_of_sale

    def place_and_points_of_sale(
        self,
    ) -> Generator[Tuple[str, List[PointOfSale]], None, None]:
        for place, points_of_sale in self.per_place.items():
            yield place, points_of_sale

    def point_of_sale(self) -> Generator[PointOfSale, None, None]:
        for point_of_sale in self.per_identifier.values():
            yield point_of_sale


def f2i(f: float) -> int:
    return int(f * 100)


def i2f(i: int) -> float:
    return i / 100


def get_price_descriptors(prices: List[PointOfSaleAndPrice]) -> Tuple[int, int, int]:
    if len(prices) == 0:
        remark = "get_price_descriptors 1: len(prices) == 0"
        raise ModelsException(remark)
    ordered_prices = sorted(prices, key=lambda x: x[1])
    try:
        float_prices = [float(price) / 100 for point_of_sale, price in ordered_prices]
    except ValueError:
        remark = "get_price_descriptors 2: bad prices"
        raise ModelsException(remark)
    else:
        prices_min, prices_max = float_prices[0], float_prices[-1]
        log_float_prices = [log(pp, 10) for pp in float_prices]
        log_prices_geomean = sum(log_float_prices) / len(log_float_prices)
        prices_geomean = 10**log_prices_geomean
        return f2i(prices_min), f2i(prices_geomean), f2i(prices_max)


# class PricesTable:
#     def __init__(self) -> None:
#         self._point_of_sale_and_price: DefaultDict[
#             str, List[PointOfSaleAndPrice]
#         ] = defaultdict(list)
#
#     @property
#     def point_of_sale_and_price(self) -> DefaultDict[str, List[PointOfSaleAndPrice]]:
#         return self._point_of_sale_and_price
#
#     def add(self, article_code: str, point_of_sale: PointOfSale, price: int) -> None:
#         self.point_of_sale_and_price[article_code].append((point_of_sale, price))
#
#     def values(self) -> Generator[List[Tuple[str, PointOfSale, int]], None, None]:
#         for (
#             article_code,
#             point_of_sale_with_price,
#         ) in self.point_of_sale_and_price.items():
#             yield article_code, point_of_sale_with_price
#


class ArticleWithPrices:
    def __init__(self, article: Article, prices: List[PointOfSaleAndPrice]) -> None:
        prices_min, prices_geomean, prices_max = get_price_descriptors(prices)
        self._article: Article = article
        self._prices_min: int = prices_min
        self._prices_geomean: int = prices_geomean
        self._prices_max: int = prices_max

    @property
    def article(self) -> Article:
        return self._article

    @property
    def prices_min(self) -> int:
        return self._prices_min

    @property
    def prices_geomean(self) -> int:
        return self._prices_geomean

    @property
    def prices_max(self) -> int:
        return self._prices_max

    @property
    def label(self) -> str:
        return f"{self.article.code:s}: {self.article.brand:s}: {self.article.name:s}"


class ArticleWithPricesTable:
    def __init__(self, place: str) -> None:
        self._place: str = place
        self._article_with_prices: Dict[str, ArticleWithPrices] = dict()

    @property
    def place(self) -> str:
        return self._place

    @property
    def article_with_prices(self) -> Dict[str, ArticleWithPrices]:
        return self._article_with_prices

    def add(self, article: Article, prices: List[PointOfSaleAndPrice]) -> None:
        self.article_with_prices[article.code] = ArticleWithPrices(article, prices)

    def select_values_by_article_code(
        self, 
        article_codes: List[str]
    ) -> Generator[ArticleWithPrices, None, None]:
        for this_article_code in article_codes:
            try:
                yield self.article_with_prices[this_article_code]
            except KeyError:
                continue

    def select_values_by_prefix(
        self, 
        prefixes: List[str]
    ) -> Generator[ArticleWithPrices, None, None]:
        for this_prefix in prefixes:
            for article_code, article_with_prices in self.article_with_prices.items():
                if article_with_prices.article.name.startswith(this_prefix):
                    yield article_with_prices

    def values(self) -> Generator[ArticleWithPrices, None, None]:
        for article_code, article_with_prices in self.article_with_prices.items():
            yield article_with_prices
