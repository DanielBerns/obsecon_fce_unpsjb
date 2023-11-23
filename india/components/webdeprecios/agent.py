from components.webdeprecios.webclient import WebClient
from components.webdeprecios.receivers import Receiver
from components.webdeprecios.emitters import Emitter

class Agent:
    def __init__(self, web_client: WebClient) -> None:
        self._web_client = web_client

    @property
    def web_client(self) -> WebClient:
        return self._web_client
    
    def update(self,
               username: str,
               receiver: Receiver, 
               emitter: Emitter
               ) -> None:
        auth_headers = self.web_client.get_auth_headers(username)
        if auth_headers:
            message_count = 0
            for message in self.web_client.get_messages(auth_headers):
                receiver.receive(message)
                message_count += 1
            if message_count:
                self.web_client.clear_messages(auth_headers)
            for content in emitter.emit():
                self.web_client.publish_post(auth_headers, content)

