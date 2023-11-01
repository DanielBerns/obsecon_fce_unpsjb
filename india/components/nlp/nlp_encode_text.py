from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, TextIO, Generator

from components.core import SampleTask, TreeStore
from components.helpers import get_container
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer
from components.nlp.io import TextTXT, TokensMD, NLPContainer


class TextCode:
    def __init__(self, 
                 base: Path
                 ) -> None:
        encoded_tokens = TokensMD.read(base)
        encoded_tokens["<Initial>"] = -1
        encoded_tokens["<Final>"] = -2
        decoded_tokens = {v:k for k, v in encoded_tokens.items()}
        self._encoded_tokens = encoded_tokens
        self._decoded_tokens = decoded_tokens
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def encoded_tokens(self) -> Dict[str, int]:
        return self._encoded_tokens

    @property
    def decoded_tokens(self) -> Dict[int, str]:
        return self._decoded_tokens

    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer

    def encode(self, sample: Path) -> Generator[List[int], None, None]:
        try:
            for sentence in TextTXT.read_sentences(sample):
                encoded_sentence = [
                    self.encoded_tokens[token] 
                    for token in self.tokenizer.read(sentence)]
                yield encoded_sentence
        except Exception as message:
            print('    Error:', str(message))

    def decode(self, encoded_sentence: List[int]) -> List[str]:
        return [self.decoded_tokens[code] for code in encoded_sentence]

            
class EncodedText:
    
    filename = "encoded_text.json"
    
    @staticmethod
    def get_encoded_text_json(base: Path) -> Path:
        container = NLPContainer.get(base)
        return Path(container, EncodedText.filename)        
    
    @staticmethod
    def serialize(encoded_sentence: List[int]) -> str:
        return '[' + ','.join(str(dd) for dd in encoded_sentence) + ']\n'

    @staticmethod
    def deserialize(line: str) -> List[int]:
        array = line[1:-2]
        parts = array.split(',')
        numbers = [int(pp) for pp in parts]
        yield numbers
    
    @staticmethod
    def read(base: Path) -> Generator[List[int], None, None]:
        encoded_text_json = EncodedText.get_encoded_text_json(base)
        with open(encoded_text_json, 'r') as source:
            for line in source:
                yield EncodedText.deserialize(line)

    @staticmethod
    def write(store: TreeStore) -> None:
        encoded_text_json = EncodedText.get_encoded_text_json(store.base)
        with open(encoded_text_json, 'w') as target:
             store.start()
             text_code = TextCode(store.base)
             for sample in store.samples(first=0):
                 print(str(sample))
                 try:
                     for encoded_sentence in text_code.encode(sample):
                         line = EncodedText.serialize(encoded_sentence)
                         target.write(line)
                 except Exception as message:
                     print("  ", str(message))
             store.stop()
        print('The end!')
