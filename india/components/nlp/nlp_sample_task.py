from collections import Counter
from pathlib import Path

import pdb

from components.core import SampleTask
from components.nlp.eda import text_characters_frequency, text_characters
from components.nlp.tokenizer import Tokenizer

class NLPSampleTask(SampleTask):
    def __init__(self):
        super().__init__('NLP')
        self._store_characters: Counter = Counter()
        self._store_tokens: Counter = Counter()        
        self._tokenizer: Tokenizer = Tokenizer()
        self._iteration: int = 0
    
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
        text_txt = Path(sample, 'text.txt')
        with open(text_txt, 'r') as source:
            lines = [line[:-1] for line in source if not line.startswith('#')]
            text = '\n'.join(lines)
            sample_characters = text_characters_frequency(text)
            self.store_characters.update(sample_characters)
            for token in self.tokenizer.read(text):
                self.store_tokens[token] += 1

    def report(self, target: Path) -> None:
        super().report(target)
        nlp_md = Path(target, 'nlp.md')
        with open(nlp_md, 'w') as target:
            target.write("# NLP\n")
            target.write("## Characters\n")
            characters = ''.join(text_characters(
                ''.join([cc for cc in self.store_characters.keys()])
                ))
            target.write(characters + '\n\n')
            target.write("## Characters stats\n")
            for key in characters:
                value = self.store_characters[key]
                if ord(key) < 32:
                    target.write(f"&{ord(key):>4d}: {value:d}\n")
                elif 32 <= ord(key) < 127:
                    target.write(f">{key:>4s}: {value:d}\n")
                else:
                    target.write(f"&{ord(key):d}: {value:d}\n")
            target.write("## Tokens\n")
            max_token_length = 0
            for key, value in self.store_tokens.items():
                target.write(f"{key:s}: {value:d}\n")
                if len(key) > max_token_length:
                    max_token_length = len(key)
            target.write(f"max token length: {max_token_length:d}\n")


class NLPSampleTaskFactory:
    def __init__(self):
        self._task = NLPSampleTask()
    
    def execute(self) -> SampleTask:
        return self._task

