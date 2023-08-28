from pathlib import Path
from typing import Dict, Optional, Generator, Tuple, List, Any

from components.core import SampleTask

class GetTextSampleTask(SampleTask):
    def __init__(self, key: str) -> None:
        super().__init__("GetTextSampleTask")
        self._key = key
        self._sources: List[str] = list()
        self._text: List[Any] = list()

    @property
    def key(self):
        return self._key

    @property
    def sources(self) -> List[str]:
        return self._sources

    @property
    def text(self) -> List[Any]:
        return self._text
    
    @text.setter
    def text(self, value: List[Any]) -> None:
        self._text = value

       
class GetTextFacadeSampleTaskFactory:
    def __init__(self):
        self._task = GetTextFacadeSampleTask()
    
    def execute(self) -> SampleTask:
        return self._task


class GetTextFacadeSampleTask(SampleTask):
    CATALOG: Optional[Dict[str, GetTextSampleTask]] = None
    
    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)
        if GetTextFacadeSampleTask.CATALOG is None:
            GetTextFacadeSampleTask.CATALOG = {}
        
    def add(self, task: GetTextSampleTask) -> None:
        GetTextFacadeSampleTask.CATALOG[task.key] = task         

    def execute(self, sample: Path) -> None:
        super().execute(sample)
        key = sample.parts[-5]
        sample_task: Optional[SampleTask] = GetTextFacadeSampleTask.CATALOG.get(key, None)
        if sample_task:
            sample_task.execute(sample)
        
    def sources(self) -> Generator[Tuple[str, List[str]], None, None]:
        for key, sample_task in GetTextFacadeSampleTask.CATALOG.items():
            yield key, sample_task.sources



