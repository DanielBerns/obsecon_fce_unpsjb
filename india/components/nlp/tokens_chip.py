from collections import Counter
from pathlib import Path
from typing import List, Dict

from components.core import SampleTask
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer
from components.nlp.io import TextTXT, CharactersMD, TokensMD, NLPContainer


class TokensChip:
    def __init__(self) -> None:
        super().__init__(identifier)
        self._tokens: Counter = Counter()
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def tokens(self) -> Counter:
        return self._tokens

    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer

    def execute(self, sample: Path) -> None:
        text = TextTXT.read(sample)
        for token in self.tokenizer.read(text):
            self.tokens[token] += 1

    def stop(self, base: Path) -> None:
        TokensMD.write(base, self.tokens)


