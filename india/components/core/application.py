import logging
from contextlib import contextmanager
from typing import Generator
from components.core.filesystem import FileSystem
from components.core.config import Config
from components.helpers import get_resource_with_timestamp


class Application:
    def __init__(self, fs: FileSystem, cfg: Config):
        self._fs = fs        
        self._config = cfg
        
    @property
    def fs(self) -> FileSystem:
        return self._fs
    
    @property
    def config(self) -> Config:
        return self._config


@contextmanager    
def create_application(
    context: str,
    version: str,
    identifier: str,
    mode: str = "live",
    dotenv: str = ".env"
    ) -> Generator[Application, None, None]:

    fs = FileSystem(context, version, mode)
    fs.metadata.start()
    cfg = Config(fs.home, mode, dotenv)

    logs_txt = get_resource_with_timestamp(fs.logs, identifier, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=cfg.log_level
    )

    logging.info(f"start")
    app = Application(fs, cfg)    
    print("app started!")    
    try:
        yield app
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        fs.metadata.stop()
        logging.info(f"stop")
        print("app stopped!")    
