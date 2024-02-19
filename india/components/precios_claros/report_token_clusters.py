import logging
from pathlib import Path
from typing import List, Dict, Generator, Tuple

from components.helpers import get_container, get_resource, classname, read_text_lines

from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import (
    SampleCollector,
    ArticleWithPricesTable,
    PointOfSale,
)
from components.core.target_template import TargetTemplate, FromStringTargetTemplate
from components.nlp.tokenizer import Tokenizer

def filename() -> str:
    return __file__[:-3]


class ReportTokenClustersError(Exception):
    pass


class TokenClustersChip:
    @staticmethod
    def get_items(
        article_with_prices_table: ArticleWithPricesTable
        ) -> Generator[Tuple[str, str, str], None, None]:
        for article_with_prices in article_with_prices_table.values():
            code = article_with_prices.article.code
            brand = article_with_prices.article.brand.strip()
            name = article_with_prices.article.name.strip()
            yield code, brand, name

    @staticmethod
    def execute(
        home: Path,
        place: str,
        article_with_prices_table: ArticleWithPricesTable,
        points_of_sale: List[PointOfSale],
    ) -> None:
        parts = place.split(":")
        city = parts[1].replace(" ", "_")
        results = Path(home, city).with_suffix('.csv')
        with open(results, 'w') as target:
             for code, brand, name in TokenClustersChip.get_items(article_with_prices_table):
                 values = "|".join((code, brand, name))
                 target.write(f"{values:s}\n")
            
        # tokens = Counter()            
        #     for a_token in name_tokens:
        #         tokens[a_token] += 1
        # sorted_tokens = sorted(tokens.keys())
        # indexed_tokens = {k: v for v, k in enumerate(sorted_tokens)}
        # for code, brand, name_tokens in self.get_items(article_with_prices_table):
        #     for a_token in name_tokens:
        #         tokens[a_token] += 1
        # sorted_tokens = sorted(tokens.keys())
        

class TokenClustersReportSample:
    def __init__(
        self, sample_collector: SampleCollector
    ) -> None:
        self._sample_collector = sample_collector

    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def execute(self, home: Path) -> None:
        sample_key = self.sample_collector.sample.sample_key
        for (
            place,
            article_with_prices_table,
            points_of_sale_table,
        ) in self.sample_collector.sample_items(home):
            token_clusters_container = get_container(
                Path(home, sample_key), "token_clusters"
            )
            TokenClustersChip.execute(
                token_clusters_container, 
                place, article_with_prices_table, points_of_sale_table
            )
