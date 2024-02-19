import unittest

from context import components
from components.core import MessageDocument, RowDocument

import json
from pathlib import Path
from typing import Dict, Protocol, Any, Generator, List, DefaultDict

class MessageArray:
    def __init__(self) -> None:
        self._messages: List[Dict[str, str]] = [{"a": "1", "b": "2"},
                                             {"a": "3", "b": "4"},
                                             {"a": "5", "b": "6"},
                                             ]
    def messages(self) -> Generator[Dict[str, str], None, None]:
        """A message is dictionary with str keys and str values."""
        for a_message in self._messages:
            yield a_message

    def start(self) -> None:
        """Placeholder for operations to perform before using the generator."""
        pass

    def stop(self) -> None:
        """Placeholder for operations to perform after using the generator."""
        pass

    
class TestMessagesAndRows(unittest.TestCase):

    def setUp(self) -> None:
        self.some_messages = MessageDocument(Path('~', 'Info', 'juliet', 'messages').expanduser())
        self.some_rows = RowDocument(Path('~', 'Info', 'juliet', 'rows').expanduser())

    def tearDown(self) -> None:
        pass

    def test(self):
        self.some_messages.update(MessageArray())
        self.some_rows.write(self.some_messages)

if __name__ == "__main__":
    unittest.main() 
