from typing import Dict, List, Generator
from components.webdeprecios.agent import Agent
from components.webdeprecios.webclient import WebClient

class Printer:
    def __init__(self)-> None:
        pass
    
    def receive(self, message: Dict[str, str]) -> None:
        for key, value in message.items():
            print(f"{str(key):s}: {str(value):s}")
    
class Publisher:
    def __init__(self, commands: List[str]) -> None:
        self._commands: List[str] = commands
    
    def emit(self) -> Generator[str, None, None]:
        for command in self._commands:
            yield command

    
def update(website: str, 
           username: str,
           commands: List[str]) -> None:
    client = WebClient(website)
    agent = Agent(client)    
    receiver = Printer()
    emitter = Publisher(commands)    
    agent.update(username, receiver, emitter)
