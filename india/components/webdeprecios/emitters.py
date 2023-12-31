from typing import Generator, Protocol


class Emitter(Protocol):
    def emit(self) -> Generator[str, None, None]:
        yield from ()
