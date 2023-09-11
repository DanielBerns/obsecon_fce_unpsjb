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
    
    root = str(Path("~", "Info").expanduser())

    @staticmethod
    def get_home(
        context: str,
        version: str,
        instance: str,
        ) -> Path:
        home = Path(FileSystem.root, context, version, instance).expanduser()
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home
    
    def __init__(self, context: str, 
                       version: str, 
                       instance: str) -> None:    
        self._context: str = context
        self._version: str = version
        self._instance: str = instance
        self._catalog: Dict[str, Path] = {}   
        self._home = FileSystem.get_home(context, version, instance)
        self._commands = get_container(self.home, "Commands")
        self._storage = get_container(self.home, "Storage")
        self._results = get_container(self.home, "Results")
        self._reports = get_container(self.home, "Reports")
        self._logs = get_container(self.home, "Logs")

    @property
    def context(self) -> str:
        return self._context

    @property
    def version(self) -> str:
        return self._version

    @property
    def instance(self) -> str:
        return self._instance

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
        return self._logs

    def clear(self) -> None:
        if self.home.exists():
            remove_directory(home)
