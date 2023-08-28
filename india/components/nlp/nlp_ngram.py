from typing import List, Tuple, Generator
from pathlib import Path
from collections import Counter
from components.nlp.nlp_encode_text import EncodedText, TextCode
from components.nlp.formats import NLPContainer

class Bigrams:
    first: int = -1
    last: int = -2

    @staticmethod    
    def get(sentence: List[int]) -> Generator[Tuple[int, int], None, None]:
        if sentence :
            for a, b in zip(sentence[:-1], sentence[1:]):
                yield a, b
            yield Bigrams.first, sentence[0]
            yield sentence[-1], Bigrams.last

    @staticmethod    
    def find_bigrams(base: Path) -> Counter:
        bigrams_frequency = Counter()
        number = 0
        for sentences in EncodedText.read(base):
            for a_sentence in sentences:
                for code in Bigrams.get(a_sentence):
                    bigrams_frequency[code] += 1
            number += 1
            if number % 1000:
                print(number)
        return bigrams_frequency
            
    @staticmethod                
    def write_frequency(base: Path, bigrams_frequency: Counter) -> None:
        container = NLPContainer.get(base)
        bigrams_frequency_md = Path(container, 'bigrams_frequency.md')
        with open(bigrams_frequency_md, 'w') as target:
            target.write("# bigrams' frequency\n")
            for a_bigram, frequency in bigrams_frequency.items():
                target.write(f"{str(a_bigram):s}{NLPContainer.separator:s}{frequency:d}\n") 

    @staticmethod                        
    def sort_bigrams(bigrams_frequency: Counter) -> List[Tuple[int, Tuple[int, int]]]:
        return sorted((v, k) for k, v in bigrams_frequency.items())
    
    @staticmethod                
    def write_sorted_bigrams(base: Path, sorted_bigrams: List[Tuple[int, Tuple[int, int]]]) -> None:
        container = NLPContainer.get(base)
        text_code = TextCode(base)
        sorted_bigrams_md = Path(container, 'sorted_bigrams.md')        
        with open(sorted_bigrams_md, 'w') as target:
            target.write("# sorted bigrams\n")
            for frequency, encoded_phrase in sorted_bigrams:
                phrase = ' '.join(text_code.decode(encoded_phrase))
                target.write(f"{phrase:s} {NLPContainer.separator:s} {frequency:d}\n") 
    
