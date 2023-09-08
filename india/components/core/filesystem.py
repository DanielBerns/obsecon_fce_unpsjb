from pathlib import Path
import sys
from typing import Optional

from components.helpers import (
    remove_directory,
    get_container,
    get_resource_identifier,
    get_timestamp,
)


class FileSystem:
    
    info_root = str(Path("~", "Info").expanduser())
    apps_root = str(Path("~", "Apps").expanduser())

    @staticmethod
    def get_info_home(
        context: str,
        version: str,
        instance: str,
        ) -> Path:
        home = Path(FileSystem.info_root, context, version, instance).expanduser()
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home
    
    @staticmethod
    def get_application_home(
        context: str,
        version: str,
        instance: str,
        ) -> Path:
        home = Path(FileSystem.apps_root, context, version, instance).expanduser()
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home
    
    def __init__(self, context: str, 
                       version: str, 
                       instance: str) -> None:    
        self._application_home: Path = FileSystem.get_application_home(context, version, instance)
        self._info_home: Path = FileSystem.get_info_home(context, version, instance)
        self._commands: Path = get_container(self.info_home, "Commands")
        self._sources: Path = get_container(self.info_home, "Sources")
        self._results: Path = get_container(self.info_home, "Results")
        self._reports: Path = get_container(self.info_home, "Reports")
        self._logs: Path = get_container(self.info_home, "Logs")

    @property
    def application_home(self) -> Path:
        return self._application_home

    @property
    def info_home(self) -> Path:
        return self._info_home

    @property
    def commands(self) -> Path:
        return self._commands

    @property
    def sources(self) -> Path:
        return self._sources

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
        if self.sources.exists():
            remove_directory(self.sources)
        if self.results.exists():
            remove_directory(self.results)
        if self.reports.exists():
            remove_directory(self.reports)
        if self.logs.exists():
            remove_directory(self.logs)
