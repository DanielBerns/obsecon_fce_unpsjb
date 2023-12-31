from typing import Optional, Generic, TypeVar, Callable

T = TypeVar("T")


class Maybe(Generic[T]):
    def __init__(self, value: Optional[T] = None) -> None:
        self._value: Optional[T] = value

    @property
    def value(self) -> Optional[T]:
        return self._value

    def bind(self, function: Callable[[T], T]) -> "Maybe":
        result = self
        if self.value:
            result = Maybe.wrap(function(self.value))
        return result

    def unwrap(self) -> Optional[T]:
        return self.value

    def __repr__(self):
        return f"Maybe({self.value})"

    @staticmethod
    def wrap(value: Optional[T]) -> "Maybe":
        return Maybe(value)


# if __name__ == '__main__':
#     maybe = Maybe.wrap(4).bind(lambda x: 2*x).bind(lambda y: y+1)
#     print(maybe)
#     print(maybe.unwrap())
#     maybe = Maybe.wrap(2.8).bind(lambda x: 2*x).bind(lambda y: y+1)
#     print(maybe)
#     print(maybe.unwrap())
