from pathlib import Path
import logging
from contextlib import contextmanager
from typing import Dict, List, Tuple, Generator

from context import components

from components.core import Config, FileSystem, Metadata
from components.helpers import (get_container, 
                                get_timestamp,
                                get_resource, 
                                get_resource_with_timestamp)


class PreciosClarosException(Exception):
    def __init__(self, explanation: Dict[str, str]) -> None:
        super().__init__(self)
        self._explanation = explanation if explanation else {"error_message": "empty explanation"}

    @property
    def explanation(self) -> Dict[str, str]:
        return self._explanation    

    def __str__(self) -> str:
        return json.dumps(self.explanation)


class FSPreciosClaros(FileSystem):
    def __init__(self, 
                 context: str,
                 version: str,
                 instance: str) -> None:
        super().__init__(context, version, instance)
        self._crontab = get_container(self.commands, "crontab")
        self._crontab_txt = get_resource(self.crontab, "crontab", ".txt")
        self._update_app_sh = get_resource(self.commands, "update_app", ".sh")
        precios_claros_commands = get_container(self.commands, "precios_claros")
        self._run_bots_sh = get_resource(precios_claros_commands, "run_bots", ".sh")
        precios_claros_storage = get_container(self.storage, "precios_claros")
        self._precios_claros = precios_claros_storage
        self._metadata = Metadata(get_container(precios_claros_storage, "metadata"))
        
    @property
    def crontab(self) -> Path:
        return self._crontab

    @property
    def crontab_txt(self) -> Path:
        return self._crontab_txt

    @property
    def update_app_sh(self) -> Path:
        return self._update_app_sh

    @property
    def run_bots_sh(self) -> Path:
        return self._run_bots_sh

    @property
    def precios_claros(self) -> Path:
        return self._precios_claros

    @property
    def metadata(self) -> Metadata:
        return self._metadata


class AppPreciosClaros:
    def __init__(self, fs: FSPreciosClaros) -> None:
        self._fs: FSPreciosClaros = fs
        self._config = Config(fs.home)

    @property
    def fs(self) -> FSPreciosClaros:
        return self._fs
    
    @property
    def config(self) -> Config:
        return self._config


@contextmanager
def create_app(
    context: str,
    version: str,
    instance: str,
    name: str) -> Generator[AppPreciosClaros, None, None]:

    fs = FSPreciosClaros(context, version, instance)
    fs.metadata.start()
    fs.metadata.add(get_timestamp(), name, "start")
    app = AppPreciosClaros(fs)

    logs_txt = get_resource_with_timestamp(fs.logs, name, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        level=app.config.log_level
    )
    
    logging.info(f"start")
    try:
        yield app
    except Exception as message:
        logging.warning(f"Warning: {str(message):s}")
    finally:
        fs.metadata.add(get_timestamp(), name, "stop")        
        fs.metadata.stop()
        logging.info(f"stop")
