from pathlib import Path
import logging
from contextlib import contextmanager
from typing import List, Tuple, Generator

from context import components

from components.core import Config, FileSystem
from components.helpers import (get_container, 
                                get_resource, 
                                get_resource_with_timestamp)


class NLPNews(Application):
    def __init__(self, 
                 context: str,
                 version: str,
                 instance: str) -> None:
        super().__init__(context, version, instance)
        self._crontab = get_container(self.fs.commands, "crontab")
        self._crontab_txt = get_resource(self.crontab, "crontab", ".txt")
        self._metadata = get_container(self.fs.storage, "metadata")
        self._news = get_container(self.fs.storage, "news")
        self._telegram = get_container(self.fs.storage, "telegram")
        self._nlp = get_container(self.fs.results, "nlp")

    @property
    def crontab(self) -> Path:
        return self._crontab

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    @property
    def metadata(self) -> Path:
        return self._metadata

    @property
    def news(self) -> Path:
        return self._news

    @property
    def telegram(self) -> Path:
        return self._telegram

    @property
    def nlp(self) -> Path:
        return self._nlp


@contextmanager
def create_nlp_news(
    context: str,
    version: str,
    instance: str,
    name: str) -> Generator[App, None, None]:

    nlp_news = NLPNews(context, version, instance)
    
    logs_txt = get_resource_with_timestamp(nlp_news.fs.logs, name, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        level=nlp_news.config.log_level
    )

    logging.info(f"start")
    try:
        yield nlp_news
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        logging.info(f"stop")
