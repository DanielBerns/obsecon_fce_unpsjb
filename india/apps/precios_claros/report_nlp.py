import logging
from pathlib import Path
from typing import Optional

from jinja2 import Template

from context import components
from components.core import SampledDataset
from components.helpers import get_container, get_resource
from components.nlp import NLP

from precios_claros_app import create_app
from sampler import PreciosClarosSample
from report_sampler import SampleCollector, ArticleWithPricesTable, PointsOfSaleTable
from writers import writer_with_target_format, TargetFormat

def filename() -> str:
    return __file__[:-3]


class NLPTargetFormat:
    def __init__(self):
        pass
    
    @property
    def template(self) -> str:
        return """{% for value, key in info %}{{ key }} : {{value}}\n{% endfor %}
                  docs: {{docs}}
               """
               
    @property
    def suffix(self) -> str:
        return ".md"


class NLPTarget:
    
    def __init__(self, home: Path) -> None:
        self._home = home
        self._target_format: Optional[TargetFormat] = None
        self._nlp = NLP()
        
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
    def nlp(self) -> NLP:
        return self._nlp
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass

    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: PointsOfSaleTable
                ) -> None:

        for article in article_with_prices.values():
            text = article.article.name
            self.nlp.update(text)
 
        template = Template(self.target_format.template)                
        content = template.render(info=sorted_tokens, docs=self.nlp.docs)
        target_container = get_container(self.home, 'nlp')
        name = place.replace(' ', '_')                                         
        nlp_file = get_resource(target_container, name, self.target_format.suffix)
        with open(nlp_file, 'w') as target:
            target.write(content)
            
            


class NLPReportSample:
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
        for place, article_with_prices, points_of_sale in self.sample_collector.execute(home, sample_key):
            nlp_target = NLPTarget(target_container)
            nlp_target.target_format = NLPTargetFormat()
            nlp_target.start()
            nlp_target.execute(place, article_with_prices, points_of_sale)
            nlp_target.stop()
            
