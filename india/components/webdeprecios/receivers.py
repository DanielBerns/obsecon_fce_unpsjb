from typing import Dict, Protocol

class Receiver(Protocol):
    def receive(self, message: Dict[str, str]) -> None:
        pass
    
    
