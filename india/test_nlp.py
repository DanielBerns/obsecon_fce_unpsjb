from collections import Counter
from pathlib import Path
from components.helpers import get_container
from components.website_agent.website_bot import WebsiteBot
from components.nlp import (text_characters,
                            text_characters_frequency,
                            Tokenizer)

from components.core import TreeStoreProcessor

class GetStoreTokensTask:
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


def get_store_tokens(bot_home: Path, identifier: str) -> GetStoreTokensTask:
    bot = WebsiteBot(bot_home, identifier)
    bot.store.start()
    sample_task = GetStoreTokensTask()
    dataset_processor = TreeStoreProcessor(bot.store, sample_task)
    dataset_processor.metadata.next_to_process = 0
    dataset_processor.execute()
    bot.store.stop()
    return sample_task


TOKEN_CHARACTERS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÑÓÚáäéëíïñòóöùúü"

if __name__ == '__main__':
    bot_home = Path('~', 'Data', 'observatorio-economico').expanduser()
    identifier = 'adnsur'
    processor_home = get_container(Path(bot_home, 'adnsur'), 'nlp')
    sample_task = get_store_tokens(bot_home, identifier)
    with open(Path(processor_home, 'stats.txt'), 'w') as target:
        for key, value in sample_task.store_characters.items():
            a_char = key if 32 <= ord(key) < 256 else '#' + str(ord(key))
            line = f"{a_char:>8s} - {ord(key):>8d}: {value:d}\n"
            target.write(line)
    with open(Path(processor_home, 'separators.txt'), 'w') as target:
        characters = sorted([key for key in sample_task.store_characters.keys()])
        separators = [c for c in characters if not c in TOKEN_CHARACTERS]
        for a_char in separators:
            target.write(f"{ord(a_char):d}\n")
    with open(Path(processor_home, 'tokens.txt'), 'w') as target:
        store_tokens = sample_task.store_tokens        
        sorted_tokens = sorted([key for key in store_tokens.keys()])
        for a_token in sorted_tokens:
            target.write(f"{a_token:s}:{store_tokens[a_token]:d}\n")

