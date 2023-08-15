from pathlib import Path
from components.helpers import get_container
from components.nlp.get_tokens_task import get_tokens_task, GetTokensTask

class NLPRun:
    def __init__(self,
                 bot_home: Path,
                 processor_home: Path
                 )
        self._bot_home = bot_home
        self._processor_home = processor_home
        
    @property
    def bot_home(self):
        return self._bot_home
        
    @property
    def processor_home(self):
        return self._processor_home

    def write_characters_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'characters.txt'), 'w') as target:
            for key, value in sample_task.store_characters.items():
                a_char = key if 32 <= ord(key) < 256 else '#' + str(ord(key))
                line = f"{a_char:>8s} - {ord(key):>8d}: {value:d}\n"
                target.write(line)

    def write_separators_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'separators.txt'), 'w') as target:
            characters = sorted([key for key in sample_task.store_characters.keys()])
            separators = [c for c in characters if not c in token_characters]
            for a_char in separators:
                target.write(f"{ord(a_char):d}\n")

    def write_tokens_txt(self, sample_task: GetTokensTask, results_home: Path):
        with open(Path(results_home, 'tokens.txt'), 'w') as target:
            store_tokens = sample_task.store_tokens        
            sorted_tokens = sorted([key for key in store_tokens.keys()])
            for a_token in sorted_tokens:
                target.write(f"{a_token:s}:{store_tokens[a_token]:d}\n")
    
    def execute(self,
        identifier: str,
        token_characters: str
        ) -> None:
        sample_task = get_tokens_task(self.bot_home, identifier)
        results_home = get_container(self.processor_home, identifier)
        self.write_characters_txt(sample_task, results_home)
        self.write_separators_txt(sample_task, results_home)
        self.write_tokens_txt(sample_task, results_home)
        
