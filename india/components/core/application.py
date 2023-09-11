from components.core.filesystem import FileSystem
from components.core.config import Config

class Application:
    def __init__(self, fs: FileSystem):
        self._fs = fs        
        self._config = Config(self.fs.home)
        
    @property
    def fs(self) -> FileSystem:
        return self._fs
    
    @property
    def config(self) -> Config:
        return self._config
    
