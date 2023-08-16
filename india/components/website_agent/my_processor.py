from components.core import (
    TreeStore,
    TreeStoreProcessor
)

from components.website_agent.website_bot import WebsiteBot
from components.helpers import get_container

from pathlib import Path


class MySampleTask:
    def __init__(self, 
                 processor_home: Path, 
                 identifier: str):
        self._results_home = get_container(processor_home, identifier)

    @property
    def results_home(self) -> Path:
        return self._results_home

    def execute(self, sample: Path) -> None:
        pass


class MyProcessor:
    def __init__(self,
                 bot_home: Path,
                 processor_home: Path
                 ) -> None:
        self._bot_home = bot_home
        self._processor_home = processor_home
        
    @property
    def bot_home(self) -> Path:
        return self._bot_home
        
    @property
    def processor_home(self) -> Path:
        return self._processor_home

    def run_sample_task(self, identifier: str) -> SampleTask:
        bot = WebsiteBot(self.bot_home, identifier)
        bot.store.start()
        sample_task = self.build_sample_task(identifier)
        dataset_processor = TreeStoreProcessor(bot.store, sample_task)
        dataset_processor.execute()
        bot.store.stop()
        return sample_task

    def build_sample_task(self, identifier: str) -> SampleTask:
        return MySampleTask(self.processor_home, identifier)

    def execute(self, identifier: str) -> None:
        sample_task = run_sample_task(identifier)
