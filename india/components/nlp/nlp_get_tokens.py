from collections import Counter
from pathlib import Path
from typing import List, Dict

from components.core import SampleTask
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer
from components.nlp.formats import TextTXT, CharactersMD, TokensMD, NLPContainer

                
class GetTokensSampleTask(SampleTask):

    def __init__(self, identifier: str) -> None:
        super().__init__(identifier)
        self._store_characters: Counter = Counter()
        self._store_tokens: Counter = Counter()        
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def store_characters(self) -> Counter:
        return self._store_characters

    @property
    def store_tokens(self) -> Counter:
        return self._store_tokens

    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer
    
    def execute(self, sample: Path) -> None:
        super().execute(sample)
        text = TextTXT.read(sample)
        sample_characters = text_characters_frequency(text)
        self.store_characters.update(sample_characters)
        for token in self.tokenizer.read(text):
            self.store_tokens[token] += 1

    def stop(self, base: Path) -> None:
        super().stop(base)
        CharactersMD.write(base, self.store_characters)
        TokensMD.write(base, self.store_tokens)


class GetTokensSampleTaskFactory:
    def __init__(self):
        self._task = GetTokensSampleTask()
    
    def execute(self) -> SampleTask:
        return self._task

