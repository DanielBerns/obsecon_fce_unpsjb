from pathlib import Path
import sys
from typing import Optional

from components.helpers import remove_directory


class FileSystem:

    def __init__(self, 
                 application_home: Path,
                 info_home: Path
                 ) -> None:
        self._application_home = application_home        
        self._info_home: Path = info_home
        self._data: Path = Path(info_home, 'Data')
        self._results: Path = Path(info_home, 'Results')
        self._reports: Path = Path(info_home, 'Reports')
        self._logs: Path = Path(info_home, 'Logs')

        self.data.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.results.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.reports.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.logs.mkdir(mode=0o700, parents=True, exist_ok=True)

    @property
    def application_home(self) -> Path:
        return self._application_home

    @property
    def info_home(self) -> Path:
        return self._info_home
    
    @property
    def data(self) -> Path:
        return self._data

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
        return self.home.parts[-2]
        
    @property
    def version(self) -> str:
        return self.home.parts[-1]
       
    def clear(self) -> None:
        if self.data.exists():
            remove_directory(self.data)
        if self.results.exists():
            remove_directory(self.results)
        if self.reports.exists():
            remove_directory(self.reports)
        if self.logs.exists():
            remove_directory(self.logs)            
