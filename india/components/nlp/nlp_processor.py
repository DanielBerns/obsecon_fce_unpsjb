from pathlib import Path
from collections import Counter

from components.helpers import get_container
from components.nlp import Tokenizer

class GetTokensTask:
    def __init__(self):
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
        text_txt = Path(sample, 'text.txt')
        with open(text_txt, 'r') as source:
            lines = [line[:-1] for line in source if not line.startswith('#')]
            text = '\n'.join(lines)
            sample_characters = text_characters_frequency(text)
            self.store_characters.update(sample_characters)
            for token in self.tokenizer.read(text):
                self.store_tokens[token] += 1


class NLPProcessor(MyProcessor):
    def __init__(self,
                 bot_home: Path,
                 processor_home: Path,
                 token_characters: str
                 ) -> None:
        super().__init__(bot_home, processor_home)
        self._token_characters = token_characters
        
    @property
    def token_characters(self) -> str:
        return self._token_characters
    
    @token_characters.setter
    def token_characters(self, value: str) -> None:
        self._token_characters = value

    def write_characters_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'characters.txt'), 'w') as target:
            for key, value in sample_task.store_characters.items():
                a_char = key if 32 <= ord(key) < 256 else '#' + str(ord(key))
                line = f"{a_char:>8s} - {ord(key):>8d}: {value:d}\n"
                target.write(line)

    def write_separators_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'separators.txt'), 'w') as target:
            characters = sorted([key for key in sample_task.store_characters.keys()])
            separators = [c for c in characters if not c in self.token_characters]
            for a_char in separators:
                target.write(f"{ord(a_char):d}\n")

    def write_tokens_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'tokens.txt'), 'w') as target:
            store_tokens = sample_task.store_tokens        
            sorted_tokens = sorted([key for key in store_tokens.keys()])
            for a_token in sorted_tokens:
                target.write(f"{a_token:s}:{store_tokens[a_token]:d}\n")
    
    def execute(self, identifier: str) -> None:
        sample_task = self.run_sample_task(identifier)
        results_home = get_container(self.processor_home, identifier)
        self.write_characters_txt(sample_task, results_home)
        self.write_separators_txt(sample_task, results_home)
        self.write_tokens_txt(sample_task, results_home)
        
    def get_sample_task(self, identifier: str) -> SampleTask:
        return GetTokensTask()
