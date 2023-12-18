from pathlib import Path
import logging
from contextlib import contextmanager
from typing import Dict, List, Tuple, Generator


from components.core import (CLIConfig, 
                             Config, 
                             build_cli_config, 
                             FileSystem, 
                             Metadata)
from components.helpers import (get_container, 
                                get_timestamp,
                                get_resource, 
                                get_resource_with_timestamp)


class FSPreciosClaros(FileSystem):
    def __init__(self, 
                 context: str,
                 version: str,
                 mode: str) -> None:
        super().__init__(context, version, mode)

        self._crontab = get_container(self.commands, "crontab")
        self._crontab_txt = get_resource(self.crontab, "crontab", ".txt")
        
        precios_claros_templates = get_container(Path('~', 'Apps', context, version), "templates")
        self._template_run_precios_claros_bot_sh = get_resource(precios_claros_templates, "run_precios_claros_bot", ".sh")

        precios_claros_commands = get_container(self.commands, "precios_claros")        
        self._run_precios_claros_bot_sh = get_resource(precios_claros_commands, "run_precios_claros_bot", ".sh")

        self._precios_claros = get_container(self.storage, "precios_claros")
        
        self._logs_txt = get_resource_with_timestamp(self.logs, "precios_claros", '.txt')

    @property
    def crontab(self) -> Path:
        return self._crontab

    @property
    def template_run_precios_claros_bot_sh(self) -> Path:
        return self._template_run_precios_claros_bot_sh
        
    @property
    def run_precios_claros_bot_sh(self) -> Path:
        return self._run_precios_claros_bot_sh

    @property
    def precios_claros(self) -> Path:
        return self._precios_claros

    @property
    def logs_txt(self) -> Path:
        return self._logs_txt


class AppPreciosClaros:
    def __init__(self, fs: FSPreciosClaros, cfg: Config, args: Dict[str, str]) -> None:
        self._fs: FSPreciosClaros = fs
        self._cfg: Config = cfg
        self._cli_args: Dict[str, str] = args

    @property
    def fs(self) -> FSPreciosClaros:
        return self._fs
    
    @property
    def cfg(self) -> Config:
        return self._cfg
    
    @property
    def cli_args(self) -> Dict[str, str]:
        return self._cli_args


@contextmanager
def create_app(
    context: str,
    version: str,
    name: str) -> Generator[AppPreciosClaros, None, None]:

    cli_cfg = build_cli_config()
    args = cli_cfg.args
    
    fs = FSPreciosClaros(context, version, args["mode"])
    fs.metadata.start()
    cfg = Config(fs.home, args["mode"], args["dotenv"])

    logging.basicConfig(
        filename=fs.logs_txt, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",        
        level=logging.DEBUG
    )

    logging.info(f"start")
    app = AppPreciosClaros(fs, cfg, args)    
    print("app started!")    
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        fs.metadata.stop()
        logging.info(f"stop")
        print("app stopped!")    
