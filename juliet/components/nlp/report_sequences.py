import logging
from pathlib import Path
from typing import List, Dict, Generator, Tuple

from components.helpers import get_container, get_resource, classname, read_text_lines



class ReportSequences:
    def __init__(
        self, 
        origin: Path,
        target: Path
    ) -> None:
        self._origin: Path = origin
        self._target: Path = target
        
    @property
    def origin(self) -> Path:
        return self._origin

    @property
    def target(self) -> Path:
        return self._target
    
    def execute() -> None:
        container = Path('.')
        nlp = build_NLP(self.origin)
        nlp.process(container, display_name, max_length=2)


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
