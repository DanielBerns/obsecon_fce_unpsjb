import logging
from contextlib import contextmanager
from typing import Generator, Dict
from components.core.filesystem import FileSystem
from components.configuration import Settings, CLI, Constants
from components.helpers import get_resource_with_timestamp

import pdb

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
    def settings(self) -> Dict[str, str]:
        return self._settings

@contextmanager    
def create_application(
    identifier: str,    
    arguments: Dict[str, str]
    ) -> Generator[Application, None, None]:

    pdb.set_trace()
    mode, dotenv = arguments.get("mode", "live"), arguments.get("dotenv", ".env")
    settings = Settings.build(
        identifier,
        mode,
        dotenv
        )
    file_system = FileSystem(settings)
    file_system.metadata.start()

    logs_txt = get_resource_with_timestamp(file_system.logs, identifier, '.txt')
    logging.basicConfig(
        filename=logs_txt, 
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=settings["log_level"]
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
