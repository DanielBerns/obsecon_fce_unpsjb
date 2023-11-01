import logging
from pathlib import Path
from typing import Optional, List

from jinja2 import Template

from context import components
from components.core import SampledDataset
from components.helpers import get_container, get_resource

from sampler import PreciosClarosSample
from report_sampler import SampleCollector, ArticleWithPricesTable, PointOfSale
from writers import writer_with_target_format, TargetFormat

import pdb

def filename() -> str:
    return __file__[:-3]


class PrefixesTargetFormat:
    def __init__(self):
        pass
    
    @property
    def template(self) -> str:
        return """{% for pp in info %}{{ pp }}
                  {% endfor %}"""
               
    @property
    def suffix(self) -> str:
        return ".md"


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
        sorted_array = sorted(array)
        last_value = (sorted_array[0]).strip()
        for item in sorted_array[1:]:
            current_value = item.strip()
            prefix = PrefixesTarget.common_prefix(current_value, last_value)
            last_value = current_value
            if prefix:
                prefixes.append(prefix.strip())
        return prefixes
    
    def __init__(self, home: Path) -> None:
        self._home = home
        self._target_format: Optional[TargetFormat] = None
        self._partial_results = list()
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def target_format(self) -> Optional[TargetFormat]:
        return self._target_format
    
    @target_format.setter
    def target_format(self, value: TargetFormat) -> None:
        self._target_format = value

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
        prefixes = PrefixesTarget.get_prefixes(set(info))
        target_container = get_container(self.home, 'prefixes')
        prefixes_file = get_resource(target_container, 'all', self.target_format.suffix) 
        template = Template(self.target_format.template)        
        content = template.render(info=prefixes)
        with open(prefixes_file, 'w') as target:
            target.write(content)            
                

    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: List[PointOfSale]
                ) -> None:

        name = place.replace(' ', '_')
        target_container = get_container(self.home, 'prefixes')
        prefixes_file = get_resource(target_container, name, self.target_format.suffix)
        article_names = list()
        for article in article_with_prices.values():
            line = article.article.name
            article_names.append(line.strip())

        prefixes = PrefixesTarget.get_prefixes(article_names)
        
        template = Template(self.target_format.template)        
        content = template.render(info=prefixes)
        with open(prefixes_file, 'w') as target:
            target.write(content)
        
        self.partial_results.append(prefixes_file)
        

class PrefixesReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector) -> None:
        self._sample_collector = sample_collector
           
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def execute(self,
                home: Path, 
                sample_key: str) -> None:
        target_container = get_container(home, sample_key)
        for place, article_with_prices, points_of_sale in self.sample_collector.execute(home, sample_key):
            prefixes = PrefixesTarget(target_container)
            prefixes.target_format = PrefixesTargetFormat()
            prefixes.start()
            prefixes.execute(place, article_with_prices, points_of_sale)
            prefixes.stop()
            
