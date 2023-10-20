from jinja2 import Template
from typing import Protocol

class TargetTemplate(Protocol):
    def __init__(self) -> None:
        pass

    @property
    def template(self) -> Template:
        return Template("Empty TargetTemplate")        

    @property
    def suffix(self) -> str:
        return ".txt"


class FromFileTargetFormat:    
    def __init__(self, resource: Path) -> None:
        self._resource = resource

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def template(self) -> Template:
        with open(self.resource, 'r') as origin:
            return Template(origin.read())        

    @property
    def suffix(self) -> str:
        return self.resource.suffix
 

class FromStringTargetTemplate:    
    def __init__(self, string: str = "", suffix: str = ".txt") -> None:
        self._string = string
        self._suffix = suffix

    @property
    def string(self) -> str:
        return self._string

    @property
    def template(self) -> Template:
        return Template(self.string)        

    @property
    def suffix(self) -> str:
        return self._suffix
