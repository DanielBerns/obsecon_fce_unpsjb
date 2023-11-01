import logging
from pathlib import Path
from typing import List


from components.helpers import get_container, get_resource, classname

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import (SampleCollector, 
                                                     ArticleWithPricesTable, 
                                                     PointOfSale)
from components.core.target_template import TargetTemplate, FromStringTargetTemplate


def filename() -> str:
    return __file__[:-3]


class ReportPrefixesError(Exception):
    pass

class PrefixesTarget:
    
    @staticmethod
    def common_prefix(one: str, two: str) -> str:
        prefix = list()
        for a, b in zip(one, two):
            if a == b:
                prefix.append(a)
            else:
                break
        return ''.join(prefix)

    @staticmethod
    def get_prefixes(array: List[str]) -> List[str]:
        prefixes = list()                
        sorted_uniq = sorted(set(array))
        last_value = (sorted_uniq[0]).strip()
        for value in sorted_uniq[1:]:
            current_value = value.strip()
            prefix = PrefixesTarget.common_prefix(current_value, last_value)
            last_value = current_value
            if prefix:
                prefixes.append(prefix.strip())
        return prefixes

    PREFIXES_TARGET = """{% for pp in prefixes %} {{pp}}
        {% endfor %}
    """
    
    PREFIXES_TARGET_SUFFIX = ".md"
    
    def __init__(self, home: Path) -> None:
        self._home = home
        self._target_template: TargetTemplate = FromStringTargetTemplate(
            PrefixesTarget.PREFIXES_TARGET,
            suffix=PrefixesTarget.PREFIXES_TARGET_SUFFIX
            )
        self._partial_results: List[str] = list()
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def target_template(self) -> TargetTemplate:
        return self._target_template
    
    @property
    def partial_results(self) -> List[str]:
        return self._partial_results
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        info = list()
        for result_file in self.partial_results:
            with open(result_file, 'r') as result:
                for line in result:
                    info.append(line.strip())
        prefixes = PrefixesTarget.get_prefixes(info)
        target_container = get_container(self.home, 'prefixes')
        prefixes_file = get_resource(target_container, 'all', self.target_template.suffix) 
        content = self.target_template.template.render(info=prefixes)
        with open(prefixes_file, 'w') as target:
            target.write(content)            

    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: List[PointOfSale]
                ) -> None:
        pdb.set_trace()
        name = place.replace(' ', '_')
        target_container = get_container(self.home, 'prefixes')
        prefixes_file = get_resource(target_container, name, self.target_template.suffix)
        article_names = list()
        for article in article_with_prices.values():
            line = article.article.name
            article_names.append(line.strip())
        prefixes = PrefixesTarget.get_prefixes(article_names)
        content = self.target_template.template.render(info=prefixes)
        with open(prefixes_file, 'w') as target:
            target.write(content)
        self.partial_results.append(str(prefixes_file))
        

class PrefixesReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector,
                 sample: PreciosClarosSample) -> None:
        self._sample_collector = sample_collector
        self.sample_collector.update(sample)
           
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def execute(self,
                home: Path, 
                sample_key: str) -> None:
        target_container = get_container(home, sample_key)
        for place, article_with_prices, points_of_sale in self.sample_collector.sample_items(home, sample_key):
            prefixes = PrefixesTarget(target_container)
            prefixes.start()
            prefixes.execute(place, article_with_prices, points_of_sale)
            prefixes.stop()
            
