from typing import Protocol


class Task(Protocol):
    @property
    def identifier(self) -> str:
        pass

    def execute(self) -> None:
        pass
