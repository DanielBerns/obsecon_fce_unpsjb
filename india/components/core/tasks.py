from typing import Dict

class Task:
    def __init__(self, parameters: Dict) -> None:
        self._parameters = parameters
    
    @property
    def parameters(self):
        return self._parameters

    def execute(self):
        pass

