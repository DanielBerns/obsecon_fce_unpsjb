from pathlib import Path
from typing import Optional

from components.helpers import remove_directory


class FileSystem:
    @staticmethod
    def get_home(root: str,
                 application: str, 
                 version: str,
                 instance: str,
                 ) -> Path:
        home: Path = Path(root, application, version, instance).expanduser()        
       
        return home

    def __init__(self, 
                 root: str,
                 application: str, 
                 version: str, 
                 instance: str,
                 ) -> None:
        home: Path = FileSystem.get_home(root, application, version, instance)
        self._home: Path = home
        self._data: Path = Path(home, 'Data')
        self._results: Path = Path(home, 'Results')
        self._reports: Path = Path(home, 'Reports')
        self._logs: Path = Path(home, 'Logs')


        self.data.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.results.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.reports.mkdir(mode=0o700, parents=True, exist_ok=True)
        self.logs.mkdir(mode=0o700, parents=True, exist_ok=True)


    @property
    def home(self):
        return self._home
    
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
    
