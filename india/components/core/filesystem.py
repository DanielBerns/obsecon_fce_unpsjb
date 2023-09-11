from pathlib import Path
import sys
from typing import Optional

from components.helpers import (
    remove_directory,
    get_container,
    get_resource,
    get_timestamp,
)


class FileSystem:
    
    info_root = str(Path("~", "Info").expanduser())

    @staticmethod
    def get_home(
        context: str,
        version: str,
        instance: str,
        ) -> Path:
        home = Path(FileSystem.info_root, context, version, instance).expanduser()
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home
    
    def __init__(self, context: str, 
                       version: str, 
                       instance: str) -> None:    
        self._context = context
        self._version = version
        self._instance = instance
        self._home: Path = FileSystem.get_home(context, version, instance)
        self._commands: Path = get_container(self.home, "Commands")
        self._storage: Path = get_container(self.home, "Storage")
        self._results: Path = get_container(self.home, "Results")
        self._reports: Path = get_container(self.home, "Reports")
        self._logs: Path = get_container(self.home, "Logs")

    @property
    def home(self) -> Path:
        return self._home

    @property
    def commands(self) -> Path:
        return self._commands

    @property
    def storage(self) -> Path:
        return self._storage

    @property
    def results(self) -> Path:
        return self._results

    @property
    def reports(self) -> Path:
        return self._reports

    @property
    def logs(self) -> Path:
        return self._logs

    @property
    def application(self) -> str:
        return self.application_home.parts[-2]

    @property
    def version(self) -> str:
        return self.application_home.parts[-1]

    def clear(self) -> None:
        if self.commands.exists():
            remove_directory(self.commands)
        if self.storage.exists():
            remove_directory(self.sources)
        if self.results.exists():
            remove_directory(self.results)
        if self.reports.exists():
            remove_directory(self.reports)
        if self.logs.exists():
            remove_directory(self.logs)
