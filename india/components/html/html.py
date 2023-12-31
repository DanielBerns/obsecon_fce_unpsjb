from typing import Dict, Protocol, TypeVar, Generic


class Node(Protocol):
    @property
    def render(self) -> str:
        ...

    def update(self, message: Dict[str, str]) -> None:
        ...
        
    
class Attribute:
    def __init__(self, name: str, value: str) -> None:
        self._name: str = name
        self._value: str = value
        
    @property
    def name(self) -> str:
        return self._name
        
    @property        
    def value(self) -> str:
        return self._value

    @property
    def render(self) -> str:
        return f'{self.name}="{self.value:s}"'
        
    def update(self, message: Dict[str, str]) -> None:
        pass


class Text:
    def __init__(self, value: str) -> None:
        self._value: str = value
        
    @property
    def value(self) -> str:
        return self._value

    @property
    def render(self) -> str:
        return self.value

    def update(self, message: Dict[str, str]) -> None:
        pass


class Tag:
    def __init__(self, prefix: str, name: str, suffix: str) -> None:
        self._prefix: str = prefix
        self._name: str = name
        self._suffix: str = suffix
        self._attributes: Dict[str, Attribute] = {}
        
    @property
    def prefix(self) -> str:
        return self._prefix
    
    @property
    def name(self) -> str:
        return self._name

    @property
    def suffix(self) -> str:
        return self._suffix
    
    def bind(self, action: Callable[[Tag], Tag]) -> Tag:
        return action(self)

    @property
    def attributes(self) -> Dict[str, Attribute]:
        return self._attributes

    @property
    def render(self) -> str:
        body = " ".join(
            [attribute.render for key, attribute in self.attributes.items()]
        )
        return prefix + body + suffix
    
    def update(self, message: Dict[str, str]) -> None:
        pass
   

class Block:
    def __init__(self) -> None:
        self._nodes: Dict[str, Node]
        
    @property
    def nodes(self) -> Dict[str, Node]:
        return self._nodes
    
    def add_node(self) -> None
    @property
    def render(self) -> str:
        return "".join([value.render for key, value in self.nodes.items()])
    
    def update(self, message: Dict[str, str]) -> None:
        pass

    

T = TypeVar('T')


class Processor(Generic[T]):
    def __init__(self) -> None:
        self._value: Optional[T] = None
        
    @property
    def value(self) -> Optional[T]:
        return self._value
    
    @element.setter
    def value(self, update: Optional[T]) -> None:
        self._value = update
        
    def bind(self, action: Callable[[Optional[T]], Optional[T]) -> 'Processor':
        try:
            result = action(self.value)
        except Exception as message:
            logging.error(
                f"{classname(self):s}.bind({classname(action)}): {str(message):s}"
            )
            
        else:
            self.value = result
                    
        return self
