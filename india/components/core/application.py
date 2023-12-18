import logging
from contextlib import contextmanager
from typing import Generator, Dict
from components.core.filesystem import FileSystem
from components.configuration import Settings, CLI, Constants
from components.helpers import get_resource_with_timestamp


class Application:
    def __init__(self, 
                 file_system: FileSystem, 
                 settings: Dict[str, str]):
        self._file_system: FileSystem = file_system        
        self._settings: Dict[str, str] = settings
        
    @property
    def file_system(self) -> FileSystem:
        return self._file_system
    
    @property
    def settings(self) -> Settings:
        return self._settings


@contextmanager    
def create_application(
    identifier: str,    
    arguments: Dict[str, str]
    ) -> Generator[Application, None, None]:

    file_system = FileSystem(
        Constants.PROJECT, 
        Constants.VERSION, 
        arguments["mode"])
    file_system.metadata.start()
    settings = Settings.build(
        identifier,
        arguments["dotenv"]
        )

    logs_txt = get_resource_with_timestamp(fs.logs, identifier, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=cfg.log_level
    )

    logging.info(f"start")
    application = Application(file_system, settings)    
    print("application started!")    
    try:
        yield application
    except Exception as message:
        logging.warning(f"exception: {str(message):s}\n")
    finally:
        file_system.metadata.stop()
        logging.info(f"stop")
        print("app stopped!")    
