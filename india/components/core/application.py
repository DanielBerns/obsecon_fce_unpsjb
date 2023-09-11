from components.filesystem import FileSystem
from components.config import Config

class Application:
    def __init__(self, 
                 context: str, 
                 version: str, 
                 instance: str):
        self._fs = FileSystem(context, version, instance)        
        self._config = Config(self.fs.home)
        
    @property
    def fs(self) -> FileSystem:
        return self._fs
    
    @property
    def config(self) -> Config:
        return self._config
    
