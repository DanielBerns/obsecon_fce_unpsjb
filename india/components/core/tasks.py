from typing import Protocol

class Task(Protocol):
    @property
    def identifier(self) -> str:
        return self._identifier

    def execute(self) -> None:
        pass

