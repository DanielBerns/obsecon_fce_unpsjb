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

import pdb

def filename() -> str:
    return __file__[:-3]


class ReportPrefixesError(Exception):
    pass

class PrefixesTarget:
    

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
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def target_template(self) -> TargetTemplate:
        return self._target_template
    
    def save_prefixes(self, 
                      name: str, 
                      prefixes: List[str]
                      ) -> None:
        content = self.target_template.template.render(prefixes=prefixes)
        pdb.set_trace()
        target_container = get_container(self.home, 'prefixes')
        prefixes_file = get_resource(target_container, name, self.target_template.suffix)         
        with open(prefixes_file, 'w') as target:
            target.write(content)

    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: List[PointOfSale]
                ) -> None:
        chip = PrefixesChip()
        for article in article_with_prices.values():
            line = article.article.name.strip()
            chip.lines.append(line)
        parts = place.split(':')
        name = parts[1].replace(' ', '_')
        self.save_prefixes(name, chip.prefixes)
        

class PrefixesReportSample:
    def __init__(self, 
                 sample_collector: SampleCollector,
                 sample: PreciosClarosSample
                 ) -> None:
        self._sample_collector = sample_collector
        self.sample_collector.update(sample)
        
    @property
    def sample_collector(self) -> SampleCollector:
        return self._sample_collector

    def execute(self,
                home: Path,
                sample_key: str) -> None:
        for place, article_with_prices, points_of_sale in self.sample_collector.sample_items(home, sample_key):
            prefixes = PrefixesTarget(home)
            prefixes.execute(place, article_with_prices, points_of_sale)
