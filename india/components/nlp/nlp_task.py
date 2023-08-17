from collections import Counter
from pathlib import Path

from components.nlp.tokenizer import Tokenizer

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


def get_tokens_task(bot_home: Path, identifier: str) -> GetTokensTask:
    bot = WebsiteBot(bot_home, identifier)
    bot.store.start()
    sample_task = GetTokensTask()
    dataset_processor = TreeStoreProcessor(bot.store, sample_task)
    dataset_processor.metadata.next_to_process = 0
    dataset_processor.execute()
    bot.store.stop()
    return sample_task
 
