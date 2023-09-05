

from pathlib import Path
import logging
from contextlib import contextmanager
from typing import List, Tuple, Generator

from context import components

from components.core import FileSystem
from components.config import Config
from components.helpers import get_container, get_timestamp, get_resource_identifier


class AppFileSystem(FileSystem):
    def __init__(self, config: Config) -> None:
        super().__init__(config.application_home, config.info_home)
        self._crontab = get_container(self.data, "crontab")
        self._metadata = get_container(self.data, "metadata")
        self._news = get_container(self.data, "news")
        self._telegram = get_container(self.data, "telegram")
        self._twitter = get_container(self.data, "twitter")
        self._downloads = get_container(self.data, "downloads")
        self._commands_txt = self.get_commands_resource("default_commands")
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
    def twitter(self) -> Path:
        return self._twitter

    @property
    def downloads(self) -> Path:
        return self._downloads

    @property
    def commands_txt(self) -> Path:
        return self._commands_txt

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    def get_commands_resource(self, identifier: str) -> Path:
        resource = get_resource_identifier(self.commands, identifier, ".txt")
        return resource

    def get_logs_resource(self, identifier: str) -> Path:
        timestamp = get_timestamp()
        resource = get_resource_identifier(
            self.logs, f"{identifier:s}_{timestamp:s}", ".txt"
        )
        return resource

    def create_commands_txt(self, commands: List[Tuple[str, str]]) -> None:
        if not self.commands_txt.exists():
            with open(self.commands_txt, "w") as target:
                for command, identifier in commands:
                    target.write(f"{command:s},[{identifier:s}]\n")


class App:
    def __init__(self, context: str, version: str):
        config = Config(context, version)
        self.config = config
        self.fs = AppFileSystem(config)


@contextmanager
def create_app(
    context: str,
    version: str,
    identifier: str) -> Generator[App, None, None]:
    app = App(context, version)

    logging.basicConfig(
        filename=app.fs.get_logs_resource(identifier), level=app.config.log_level
    )

    logging.info(f"start {identifier:s}")
    try:
        yield app
    except Exception as message:
        logging.info(f"{str(message):s}\n")
    finally:
        logging.info(f"stop {identifier:s}")
