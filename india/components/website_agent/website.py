from dataclasses import dataclass
from typing import List

from components.core import SampleTask

@dataclass
class Website:
    identifier: str
    url: str
    pipeline: List[SampleTask]

