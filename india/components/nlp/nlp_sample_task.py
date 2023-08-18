from collections import Counter
from pathlib import Path

from components.core import SampleTask
from components.nlp.eda import text_characters_frequency
from components.nlp.tokenizer import Tokenizer

class NLPSampleTask:
    def __init__(self):
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
    
    @property
    def iteration(self) -> int:
        return self._iteration
    
    @iteration.setter
    def iteration(self, value: int) -> None:
        self._iteration = value

    def execute(self, sample: Path) -> None:
        self.iteration += 1
        print(f"NLP - {str(sample):s}: {self.iteration:d}")
        text_txt = Path(sample, 'text.txt')
        with open(text_txt, 'r') as source:
            lines = [line[:-1] for line in source if not line.startswith('#')]
            text = '\n'.join(lines)
            sample_characters = text_characters_frequency(text)
            self.store_characters.update(sample_characters)
            for token in self.tokenizer.read(text):
                self.store_tokens[token] += 1

    def report(self, target: Path) -> None:
        print(f"NLP - Total iterations {self.iteration:d}")
        nlp_md = Path(sample, 'nlp.md')
        with open(nlp_stats_md, 'w', encoding='utf-8') as target:
            target.write("# NLP\n")
            target.write("## Characters\n")
            characters = ''.join([cc for cc in self.store_characters.keys()])
            target.write(characters + '\n\n')
            target.write("## Characters stats\n")
            for key, value in self.store_characters.items():
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

