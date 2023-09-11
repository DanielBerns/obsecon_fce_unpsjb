from components.config import Config
from components.core import FileSystem

App = Tuple[Config, FileSystem]

def create_app(context: str, version: str, instance: str) -> App:
    config = Config(context, version, instance)
    fs = FileSystem(config.application_home, config.info_home)
    
    return config, fs
    
    
