import logging
from pathlib import Path
from typing import List, Dict, Generator, Tuple

from components.helpers import get_container, get_resource, classname, read_text_lines



class ReportSequences:
    def __init__(
        self, 
        origin_container: Path,
        target_container: Path
    ) -> None:
        self._origin_container: Path = origin_container
        self._target_container: Path = target_container
        
    @property
    def origin_container(self) -> Path:
        return self._origin_container

    @property
    def target_container(self) -> Path:
        return self._target_container
    
    def execute() -> None:
        container = Path('.')
        nlp = build_NLP(self.origin_container)
        nlp.process(self.target_container, max_length=2)

