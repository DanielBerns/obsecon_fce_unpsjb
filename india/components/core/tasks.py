class Task:
    def __init__(self, parameters: Dict):
        self._parameters = parameters
    
    @property
    def parameters(self):
        return self._parameters

    def execute(self):
        pass

