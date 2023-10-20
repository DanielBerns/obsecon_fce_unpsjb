from pathlib import Path
import logging
from contextlib import contextmanager
from typing import Dict, List, Tuple, Generator

from context import components

from components.core import Config, FileSystem, Metadata
from components.helpers import (get_container, 
                                get_resource, 
                                get_resource_with_timestamp)


class FSNLPNews(FileSystem):
    def __init__(self, 
                 context: str,
                 version: str,
                 mode: str) -> None:
        super().__init__(context, version, mode)
        self._crontab = get_container(self.commands, "crontab")
        self._crontab_txt = get_resource(self.crontab, "crontab", ".txt")
        self._update_app_sh = get_resource(self.commands, "update_app", ".sh")
        nlp_news_container = get_container(self.commands, "nlp_news")
        self._run_news_bots_sh = get_resource(nlp_news_container, "run_news_bots", ".sh")
        precios_claros_container = get_container(self.commands, "precios_claros")
        self._run_precios_claros_sampler_sh = get_resource(
            precios_claros_container, "run_sampler", ".sh")
        self._run_precios_claros_report_sampler_sh = get_resource(
            precios_claros_container, "run_report_sampler", ".sh")
        
        self._news = get_container(self.storage, "news")
        self._precios_claros = get_container(self.storage, "precios_claros")
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
    def update_app_sh(self) -> Path:
        return self._update_app_sh

    @property
    def run_news_bots_sh(self) -> Path:
        return self._run_news_bots_sh

    @property
    def run_precios_claros_sampler_sh(self) -> Path:
        return self._run_precios_claros_sampler_sh

    @property
    def run_precios_claros_report_sampler_sh(self) -> Path:
        return self._run_precios_claros_report_sampler_sh

    @property
    def news(self) -> Path:
        return self._news

    @property
    def precios_claros(self) -> Path:
        return self._precios_claros

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
    def __init__(self, fs: FSNLPNews, cfg: Config) -> None:
        self._fs: FSNLPNews = fs
        self._cfg: Config = cfg

    @property
    def fs(self) -> FSNLPNews:
        return self._fs
    
    @property
    def cfg(self) -> Config:
        return self._cfg


@contextmanager
def create_app(
    context: str,
    version: str,
    name: str,
    args: Dict[str, str]) -> Generator[AppNLPNews, None, None]:

    fs = FSNLPNews(context, version, args["mode"])
    fs.metadata.start()
    cfg = Config(fs.home, args)
    app = AppNLPNews(fs, cfg)

    logs_txt = get_resource_with_timestamp(fs.logs, name, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        level=app.cfg.log_level
    )

    logging.info(f"start")
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        fs.metadata.stop()
        logging.info(f"stop")
    
