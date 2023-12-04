from collections import defaultdict, Counter
from pathlib import Path
from typing import DefaultDict, List, Generator, Dict, Tuple, Optional
import math
from os import walk
import logging
from dataclasses import dataclass

from components.helpers import get_resource, get_container, i, classname
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.models import (PointOfSale, ArticleWithPrices)

from components.precios_claros.writers import (WriterWithTargetFormat,
                                               ArticleWithPricesTableHTML,
                                               ArticleWithPricesTableMD,
                                               FULL_INFO_MD,
                                               PREFIXES_MD)

import pdb

Comparison = Tuple[PointOfSale, ArticleWithPrices, ArticleWithPrices]

class ReportDeltaError(Exception):
    pass


class DeltaReportSample:
    def __init__(self) -> None:
        pass
           
    def get_categories(self, home: Path, identifier: str) -> Generator[str, None, None]:
        container = get_container(home, identifier)
        for root, dirs, files in walk(container):
            for category in dirs:
                yield category

    def next_comparison(self,
                home: Path, 
                reference_sample: PreciosClarosSample,
                current_sample: PreciosClarosSample,
                ) -> Generator[Comparison, None, None]: 
        reference_collector = SampleCollector()
        reference_collector.update(reference_sample)
        current_collector = SampleCollector()
        current_collector.update(current_sample)  
        for ref_place, ref_awp_table, ref_pos in reference_collector.sample_items(home):
            cur_awp_table = current_collector.get_article_with_prices_table(
                home, ref_place)
            for ref_awp in ref_awp_table.all_of_them():
                cur_awp = cur_awp_table.article_with_prices.get(
                    ref_awp.article.code, None)
                if cur_awp:
                    yield ref_place, ref_awp, cur_awp
                
    def execute(self,
                home: Path, 
                reference_sample: PreciosClarosSample,
                current_sample: PreciosClarosSample,
                ) -> None:
        for ref_place, ref_awp, cur_awp in self.next_comparison(
            home, reference_sample, current_sample):
            ref_ps = ref_awp.prices_stats
            cur_ps = cur_awp.prices_stats
            print(f"{ref_awp.article.code:s} - {ref_awp.article.name:s} {ref_awp.article.brand:s}")
            print(f"   {str(ref_ps[0]):s} - {str(ref_ps[1]):s} - {str(ref_ps[2]):s}")
            print(f"   {str(cur_ps[0]):s} - {str(cur_ps[1]):s} - {str(cur_ps[2]):s}")
