from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, TextIO, Generator

from components.core import SampleTask, TreeStore
from components.helpers import get_container
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer
from components.nlp.formats import TextTXT, TokensMD

# TODO
class EncodedText:
    @staticmethod
    def reader(container: Path) -> Generator[List[int], None, None]:
        encoded_text_json = Path(container, EncodedText.filename)
        with open(encoded_text_json, 'r') as source:
            for line in source:
                yield TextEncoder.deserialize(line)

    @staticmethod
    def generate(store: TreeStore) -> None:
        container = TokensMD.target_container(store.base)
        encoded_text_json = Path(container, EncodedText.filename)
        with open(encoded_text_json, 'w') as target:
             store.start()
             text_encoder = TextEncoder(container)
             for sample in store.samples():
                 for encoded_sentence in text_encoder.execute(sample):
                     line = TextEncoder.serialize(encoded_sentence)
                     target.write(line)
             store.stop()
            

class TextEncoder:
    def __init__(self, 
                 container: Path
                 ) -> None:
        super().__init__("TextEncoder")
        self._all_the_tokens = TokensMD.read(container)        
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def all_the_tokens(self) -> Dict[str, int]:
        return self._all_the_tokens

    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer

    @staticmethod
    def serialize(encoded_sentence: List[int]) -> str:
        return '[' + ','.join(str(dd) for dd in encoded_sentence) + ']\n'

    @staticmethod
    def deserialize(line: str) -> List[int]:
        array = line[1:-2]
        parts = array.split(',')
        numbers = [int(pp) for pp in parts]
        yield numbers

    def execute(self, sample: Path) -> None:
        for sentence in TextTXT.read_sentences(sample):
            encoded_sentence = []
            for token in self.tokenizer.read(sentence):
                encoded_sentence.append(self.all_the_tokens[token])
            yield encoded_sentence

# TODO


    
    
@contextmanager
def create_encoded_text_writer(base: Path) -> Generator[EncodedTextWriter, None, None]:
    container = get_container(base, 'target')
    identifier = Path(container, 'encoded_text.json')
    try:
        target = open(identifier, 'w')
        resource = EncodedTextWriter(target)
        yield resource
    except Exception as message:
        print(str(message))
    finally:
        if target.closed:
            pass
        else:
            target.close()

@contextmanager
def create_encoded_text_reader(base: Path) -> Generator[EncodedTextReader, None, None]:
    container = get_container(base, 'target')    
    identifier = Path(container, 'encoded_text.json')
    try:
        source = open(identifier, 'r')
        resource = EncodedTextReader(source)
        yield resource
    except Exception as message:
        print(str(message))
    finally:
        if source.closed:
            pass
        else:
            source.close()
    
