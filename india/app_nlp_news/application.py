

from pathlib import Path
import logging
from contextlib import contextmanager
from typing import List, Tuple, Generator

from context import components

from components.core import FileSystem
from components.config import Config
from components.helpers import (get_container, 
                                get_resource_identifier, 
                                get_resource_identifier_with_timestamp)


class AppFS(FileSystem):
    def __init__(self, 
                 context: str,
                 version: str,
                 instance: str) -> None:
        super().__init__(context, version, instance)
        self._crontab = get_container(self.sources, "crontab")
        self._metadata = get_container(self.sources, "metadata")
        self._news = get_container(self.sources, "news")
        self._telegram = get_container(self.sources, "telegram")
        self._downloads = get_container(self.sources, "downloads")
        self._commands_txt = get_resource_identifier(self.commands, "default_commands", ".txt")
        self._crontab_txt = get_resource_identifier(self.crontab, "crontab", ".txt")

    @property
    def crontab(self) -> Path:
        return self._crontab

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
    def downloads(self) -> Path:
        return self._downloads

    @property
    def commands_txt(self) -> Path:
        return self._commands_txt

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    def create_commands_txt(self, commands: List[Tuple[str, str]]) -> None:
        if not self.commands_txt.exists():
            with open(self.commands_txt, "w") as target:
                for command, identifier in commands:
                    target.write(f"{command:s},[{identifier:s}]\n")


class App:
    def __init__(self, 
                 context: str, 
                 version: str, 
                 instance: str):
        self.fs = AppFS(context, version, instance)        
        self.config = Config()


@contextmanager
def create_app(
    context: str,
    version: str,
    instance: str,
    name: str) -> Generator[App, None, None]:

    app = App(context, version, instance)
    
    logging.basicConfig(
        filename=get_resource_identifier_with_timestamp(app.fs.logs, name), 
        level=app.config.log_level
    )

    logging.info(f"start")
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        logging.info(f"stop")
