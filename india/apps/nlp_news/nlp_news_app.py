from pathlib import Path
import logging
from contextlib import contextmanager
from typing import List, Tuple, Generator

from context import components

from components.core import Config, FileSystem, Metadata
from components.helpers import (get_container, 
                                get_resource, 
                                get_resource_with_timestamp)


class FSNLPNews(FileSystem):
    def __init__(self, 
                 context: str,
                 version: str,
                 instance: str) -> None:
        super().__init__(context, version, instance)
        self._crontab = get_container(self.commands, "crontab")
        self._crontab_txt = get_resource(self.crontab, "crontab", ".txt")
        self._news = get_container(self.storage, "news")
        self._telegram = get_container(self.storage, "telegram")
        self._nlp = get_container(self.results, "nlp")
        self._metadata = Metadata(get_container(self.storage, "metadata"))
        
    @property
    def crontab(self) -> Path:
        return self._crontab

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    @property
    def news(self) -> Path:
        return self._news

    @property
    def telegram(self) -> Path:
        return self._telegram

    @property
    def nlp(self) -> Path:
        return self._nlp

    @property
    def metadata(self) -> Metadata:
        return self._metadata


class AppNLPNews:
    def __init__(self, fs: FSNLPNews) -> None:
        self._fs: FSNLPNews = fs
        self._config = Config(fs.home)

    @property
    def fs(self) -> FSNLPNews:
        return self._fs
    
    @property
    def config(self) -> Config:
        return self._config


@contextmanager
def create_app(
    context: str,
    version: str,
    instance: str,
    name: str) -> Generator[AppNLPNews, None, None]:

    fs = FSNLPNews(context, version, instance)
    fs.metadata.start()
    app = AppNLPNews(fs)
    
    logs_txt = get_resource_with_timestamp(
        fs.logs, name, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        level=app.config.log_level
    )

    logging.info(f"start")
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        fs.metadata.stop()
        logging.info(f"stop")
    
