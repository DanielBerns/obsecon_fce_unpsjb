import logging
from pathlib import Path
from typing import List


from components.helpers import get_container, get_resource, classname

from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import (SampleCollector, 
                                                     ArticleWithPricesTable, 
                                                     PointOfSale)
from components.core.target_template import (TargetTemplate, 
                                             FromStringTargetTemplate)
from components.nlp.prefixes_chip import PrefixesChip


def filename() -> str:
    return __file__[:-3]


class ReportGroupbyError(Exception):
    pass

class GroupbyTarget:
    
    GROUPBY_TARGET = """{{aa.article_code}} / {{aa.brand}} / {{aa.name}}"""
    
    GROUPBY_TARGET_SUFFIX = ".csv"
    
    def __init__(self, patterns: List[str]) -> None:
        self._target_template: TargetTemplate = FromStringTargetTemplate(
            GroupbyTarget.GROUPBY_TARGET,
            suffix=GroupbyTarget.GROUPBY_TARGET_SUFFIX
            )
        self._patterns: List[str] = patterns
    
    @property
    def target_template(self) -> TargetTemplate:
        return self._target_template

    @property
    def patterns(self) -> List[str]:
        return self._patterns
    
    def execute(self, 
                home: Path,
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: List[PointOfSale]
                ) -> None:
        print(f"place: {place:s}")        
        for count_pattern, pattern in self.patterns:
            print(f"#pattern: {count_pattern:d}")    
            safe_pattern = pattern.replace(' ', '_')
            container = get_container(home, place)
            pattern_file = get_resource(container, safe_pattern, self.target_template.suffix)
            with open(pattern_file, 'w') as target:
                count_matched_articles = 0
                for article in article_with_prices.values():
                    line = article.article.name.strip()
                    if line.startswith(pattern):
                        count_matched_articles += 1
                        content = self.target_template.template.render(aa=article)
                        target.write(content + "\n")
                        print(f"#articles: {count_matched_articles:d}")
        

class GroubyReportSample:
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
        patterns_resource = get_resource(patterns_container, 'categories', '.md')
        patterns = read_text_lines(patterns_resource) 
        groupby_container = get_container(home, 'groupby')
        for place, article_with_prices, points_of_sale in self.sample_collector.sample_items(home, sample_key):
            groupby = GroupbyTarget(patterns)
            groupby.execute(groupby_container, place, article_with_prices, points_of_sale)
