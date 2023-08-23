from collections import Counter
from contextlib import contextmanager
from pathlib import Path
from typing import List, Dict, TextIO, Generator

from components.core import SampleTask
from components.helpers import get_container
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer
from components.nlp.formats import TextTXT, TokensMD


class EncodedTextReader:
    def __init__(self, source: TextIO) -> None:
        self._source = source
   
    def read(self) -> Generator[List[int], None, None]:
        for line in self._source:
            array = line[1:-2]
            parts = array.split(',')
            numbers = [int(pp) for pp in parts]
            yield number


class EncodedTextWriter:
    def __init__(self, target: TextIO) -> None:
        self._target = target
    
    def write(self, encoded_sentence: List[int]) -> None:
        text =  '[' + ','.join(str(dd) for dd in encoded_sentence) + ']\n'
        self._target.write(text)


class NLPEncodeText(SampleTask):
    def __init__(self, 
                 all_the_tokens: Dict[str, int],
                 writer: EncodedTextWriter
                 ) -> None:
        super().__init__("NLPEncodeText")
        self._all_the_tokens = all_the_tokens # TokensMD.read(container)        
        self._writer = writer
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def all_the_tokens(self) -> Dict[str, int]:
        return self._all_the_tokens

    @property
    def writer(self) -> EncodedTextWriter:
        return self._writer
    
    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer

    def execute(self, sample: Path) -> None:
        super().execute(sample)
        for sentence in TextTXT.read_sentences(sample):
            encoded_sentence = []
            for token in self.tokenizer.read(sentence):
                encoded_sentence.append(self.all_the_tokens[token])
            self.writer.write(encoded_sentence)
            
    def report(self, container: Path) -> None:
        super().report(container)


@contextmanager
def encoded_text_writer(base: Path) -> Generator[NLPEncodeText, None, None]:
    container = get_container(Path(base, 'target'))
    identifier = Path(container, 'encoded_text.json')
    try:
        target = open(identifier, 'w')
        all_the_tokens = TokensMD.read(container)
        writer = EncodedTextWriter(target)
        resource = NLPEncodeText(all_the_tokens, writer)
        yield resource
    except Exception as message:
        print(str(message)
    finally:
        if target.closed:
            pass
        else:
            target.close()

@contextmanager
def encoded_text_reader(base: Path) -> Generator[EncodedTextReader, None, None]:
    container = get_container(Path(base, 'target'))    
    identifier = Path(container, 'encoded_text.json')
    try:
        source = open(identifier, 'r')
        resource = EncodedTextReader(source)
        yield resource
    except Exception as message:
        print(str(message)
    finally:
        if source.closed:
            pass
        else:
            source.close()
    
