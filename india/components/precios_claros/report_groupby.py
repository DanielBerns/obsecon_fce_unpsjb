import logging
from pathlib import Path
from typing import List, Dict, Generator, Tuple


from components.helpers import get_container, get_resource, classname, read_text_lines

from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import (SampleCollector, 
                                                     ArticleWithPricesTable, 
                                                     PointOfSale)
from components.core.target_template import (TargetTemplate, 
                                             FromStringTargetTemplate)
import pdb

def filename() -> str:
    return __file__[:-3]


class ReportGroupbyError(Exception):
    pass

class GroupbyTarget:
    
    GROUPBY_TARGET = """{{aa.article.code}} / {{aa.article.brand}} / {{aa.article.name}} / {{aa.prices_min()}} / {{aa.prices_geomean()}} / {{aa.prices_max()}}"""
    
    GROUPBY_TARGET_SUFFIX = ".csv"
    
    def __init__(self, categories: List[str], groups: List[str]) -> None:
        self._target_template: TargetTemplate = FromStringTargetTemplate(
            GroupbyTarget.GROUPBY_TARGET,
            suffix=GroupbyTarget.GROUPBY_TARGET_SUFFIX
            )
        self._categories: List[str] = categories
        self._groups: List[str] = groups
        identifiers: Dict[str, str] = {}
        for line in self.groups:
            aa, bb = line.split(' -')
            key = aa
            value = bb.strip()
            identifiers[key] = value
        self._identifiers: Dict[str, str] = identifiers
    
    @property
    def target_template(self) -> TargetTemplate:
        return self._target_template

    @property
    def categories(self) -> List[str]:
        return self._categories

    @property
    def groups(self) -> List[str]:
        return self._groups
    
    @property
    def identifiers(self) -> Dict[str, str]:
        return self._identifiers
    
    def get_items(self) -> Generator[Tuple[int, str, str], None, None]:
        for count, (key, value) in enumerate(self.identifiers.items()):
            yield count, key, value
            
    def execute(self, 
                home: Path,
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: List[PointOfSale]
                ) -> None:
        parts = place.split(':')
        city = parts[1].replace(' ', '_')
        print(f"place: {city:s}")
        categories_container = get_container(Path(home, 'categories'), city)
        group_container = get_container(Path(home, 'groups'), city)        
        for item_counter, category, group in self.get_items():
            print(f"#category: {item_counter:d}")
            # if group == 'gatos':
            #    pdb.set_trace()
            safe_category = category.replace(' ', '_')
            category_file = get_resource(categories_container, safe_category, self.target_template.suffix)
            group_file = get_resource(group_container, group, self.target_template.suffix)
            with open(category_file, 'w') as category_target, \
                 open(group_file, 'a') as group_target:
                    count_matched_articles = 0
                    for article in article_with_prices.values():
                        line = article.article.name.strip()
                        if line.startswith(category):
                            count_matched_articles += 1
                            content = self.target_template.template.render(aa=article)
                            category_target.write(content + "\n")
                            group_target.write(content + "\n")
                            print(f"#articles: {count_matched_articles:d}")
       

class GroupbyReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector,
                 sample: PreciosClarosSample
                 ) -> None:
        self._sample_collector = sample_collector
        self.sample_collector.update(sample)
        
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def execute(self, home: Path) -> None:
        sample_key = self.sample_collector.sample.sample_key
        patterns_container = get_container(home, 'patterns')
        categories_resource = get_resource(patterns_container, 'categories', '.md')
        groups_resource = get_resource(patterns_container, 'groups', '.md')        
        categories = read_text_lines(categories_resource)
        groups = read_text_lines(groups_resource)
        groupby_container = get_container(home, 'groupby')        
        groupby = GroupbyTarget(categories, groups)        
        for place, article_with_prices, points_of_sale in self.sample_collector.sample_items(home):
            groupby.execute(groupby_container, 
                            place, 
                            article_with_prices, 
                            points_of_sale)
