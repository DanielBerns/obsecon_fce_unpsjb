from pathlib import Path
import logging

from components.core.filesystem import FileSystem
from components.config import Config
from components.helpers import get_container, get_timestamp, get_resource_identifier


DEFAULT_COMMANDS = [
  ("~/Apps/observatorio_fce_unpsjb/india/run_news_grabber.sh:36 * * * *", "run_news_grabber"),
  ("~/Apps/observatorio_fce_unpsjb/india/update_app.sh:37 * * * *", "update_app")
]

class Engine:
    def __init__(self) -> None:
        config = Config()
        fs = FileSystem(config.application_home, config.info_home)
        self._crontab = get_container(fs.data, 'crontab')
        self._metadata = get_container(fs.data, 'metadata')        
        self._news = get_container(fs.data, 'news')
        self._telegram = get_container(fs.data, 'telegram')
        self._twitter = get_container(fs.data, 'twitter')
        self._downloads = get_container(fs.data, 'downloads')
        self._config = config
        self._fs = fs

    @property
    def crontab(self):
        return self._crontab

    @property
    def metadata(self):
        return self._metadata

    @property
    def news(self):
        return self._news

    @property
    def telegram(self):
        return self._telegram

    @property
    def twitter(self):
        return self._twitter

    @property
    def downloads(self):
        return self._downloads
    
    @property
    def config(self):
        return self._config

    @property
    def fs(self):
        return self._fs

    def get_crontab_resource(self):
        crontab_txt = get_resource_identifier(
            self.crontab, 'crontab', '.txt')
        return crontab_txt
        
    def get_commands_resource(self, identifier: str) -> Path:
        resource = get_resource_identifier(
            self.fs.commands,
            identifier, 
            ".txt")
        return resource
        
    def get_logs_resource(self, identifier: str) -> Path:
        timestamp = get_timestamp()
        resource = get_resource_identifier(
            self.fs.logs, 
            f"{identifier:s}_{timestamp:s}", 
            ".txt")    
        return resource
    
    def create_default_commands(self) -> None:
        default_commands = self.get_commands_resource("default_commands")
        if not default_commands.exists():
            with open(default_commands, 'w') as target:
                for command, identifier in DEFAULT_COMMANDS:
                    target.write(f"{command:s},[{identifier:s}]\n")
