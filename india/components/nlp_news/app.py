from pathlib import Path
import logging
from contextlib import contextmanager
from typing import Dict, List, Tuple, Generator

from components.core import CLIConfig, Config, FileSystem, Metadata
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
        
        templates_container = get_container(Path('~', 'Apps', context, version), "templates")
        self._template_run_nlp_news_telegram_bot_sh = get_resource(templates_container, "run_nlp_news_telegram_bot", ".sh")
        self._template_run_nlp_news_websites_bot_sh = get_resource(templates_container, "run_nlp_news_websites_bot", ".sh")
        self._template_update_repo_sh = get_resource(templates_container, "update_repo", ".sh")
        
        nlp_news_container = get_container(self.commands, "nlp_news")        
        self._run_nlp_news_telegram_bot_sh = get_resource(nlp_news_container, "run_nlp_news_telegram_bot", ".sh")
        self._run_nlp_news_websites_bot_sh = get_resource(nlp_news_container, "run_nlp_news_websites_bot", ".sh")
        self._update_repo_sh = get_resource(self.commands, "update_repo", ".sh")
        
        self._nlp_news_telegram = get_container(self.storage, "nlp_news_telegram")
        self._nlp_news_websites = get_container(self.storage, "nlp_news_websites")
        self._nlp_news = get_container(self.results, "nlp_news")
        self._metadata = Metadata(get_container(self.storage, "metadata"))
        
    @property
    def crontab(self) -> Path:
        return self._crontab

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    @property
    def template_update_repo_sh(self) -> Path:
        return self._template_update_repo_sh

    @property
    def update_repo_sh(self) -> Path:
        return self._update_repo_sh

    @property
    def template_run_nlp_news_telegram_bot_sh(self) -> Path:
        return self._template_nlp_news_telegram_bot_sh

    @property
    def run_nlp_news_websites_bot_sh(self) -> Path:
        return self._run_nlp_news_websites_bot_sh

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
    def __init__(self, fs: FSNLPNews, cfg: Config, args: Dict[str, str]) -> None:
        self._fs: FSNLPNews = fs
        self._cfg: Config = cfg
        self._cli_args: Dict[str, str] = args

    @property
    def fs(self) -> FSNLPNews:
        return self._fs
    
    @property
    def cfg(self) -> Config:
        return self._cfg
    
    @property
    def cli_args(self) -> Dict[str, str]:
        return self._cli_args
    

@contextmanager
def create_app(
    context: str,
    version: str,
    name: str) -> Generator[AppNLPNews, None, None]:

    cli_cfg = CLIConfig()   
    cli_cfg.add_arguments()
    args = cli_cfg.args
    
    fs = FSNLPNews(context, version, args["mode"])
    fs.metadata.start()
    cfg = Config(fs.home, args)

    logs_txt = get_resource_with_timestamp(fs.logs, "nlp_news", '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        level=cfg.log_level
    )

    logging.info(f"start")
    app = AppNLPNews(fs, cfg, args)    
    print("app started!")    
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        fs.metadata.stop()
        logging.info(f"stop")
        print("app stopped!")    
