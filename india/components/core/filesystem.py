from pathlib import Path
from typing import Optional

from components.helpers import remove_directory

class FileSystem:
    def __init__(self, 
                 application: str, 
                 version: str, base: Optional[Path] = None) -> None:
        if base is None:
            base = Path('~')
        home: Path = Path(base, 'Apps', application, version).expanduser()
        self._home: Path = home
        self._data: Path = Path(home, 'Data')
        self._results: Path = Path(home, 'Results')
        self._reports: Path = Path(home, 'Reports')
        self._logs: Path = Path(home, 'logs')
        self._secrets: Path = Path(home, '.secrets')
        
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
    def secrets(self) -> Path:
        return self._secrets

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
        if self.secrets.exists():
            remove_directory(self.secrets)
    
