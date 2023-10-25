from pathlib import Path
import sys
from typing import Optional

from components.helpers import (
    remove_directory,
    get_container,
    get_resource,
    get_timestamp,
)
from components.core import Metadata


class FileSystem:
    
    root = str(Path("~", "Info").expanduser())

    @staticmethod
    def get_home(
        context: str,
        version: str,
        mode: str,
        ) -> Path:
        home = Path(FileSystem.root, context, version, mode).expanduser()
        home.mkdir(mode=0o700, parents=True, exist_ok=True)
        return home
    
    def __init__(self, context: str, 
                       version: str, 
                       mode: str) -> None:    
        self._context: str = context
        self._version: str = version
        self._mode: str = mode
        self._catalog: Dict[str, Path] = {}   
        apps = Path('~', 'Apps', 'observatorio_fce_unpsjb', 'india').expanduser()
        self._templates = get_container(apps, "templates")
        self._home = FileSystem.get_home(context, version, mode)
        self._commands = get_container(self.home, "Commands")
        self._storage = get_container(self.home, "Storage")
        self._results = get_container(self.home, "Results")
        self._reports = get_container(self.home, "Reports")
        self._logs = get_container(self.home, "Logs")
        self._metadata = Metadata(get_container(self.home, "metadata"))        

    @property
    def context(self) -> str:
        return self._context

    @property
    def version(self) -> str:
        return self._version

    @property
    def mode(self) -> str:
        return self._mode

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
    def metadata(self) -> Metadata:
        return self._metadata

    def clear(self) -> None:
        if self.home.exists():
            remove_directory(home)
