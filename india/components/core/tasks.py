class Task:
    def __init__(self, identifier: str) -> None:
        self._identifier = identifier
    
    @property
    def identifier(self) -> str:
        return self._identifier

    def execute(self):
        pass

