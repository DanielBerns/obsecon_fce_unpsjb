from typing import List, Tuple, Callable, Dict
from collections import Counter

TextMapping = Tuple[Callable[[str], List[int]], Callable[[List[int]], str]]

def text_read(source:str) -> str:
    # get text from utf-8 encoded file
    with open(source, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def text_characters(text: str) -> List:
    # here are all the unique characters that occur in this text
    return sorted(list(set(text)))

def text_characters_frequency(text: str) -> Counter:
    return Counter(text)

def text_characters_to_integers(characters: List) -> TextMapping:
    # create a mapping from characters to integers
    stoi = { ch:i for i, ch in enumerate(characters) }
    itos = { i:ch for i, ch in enumerate(characters) }
    # encoder: take a string, output a list of integers
    encode = lambda s: [stoi[c] for c in s] 
    # decoder: take a list of integers, output a string
    decode = lambda l: ''.join([itos[i] for i in l]) 
    return encode, decode


def text_fragments(text: str, width: int) -> str:
    for i in range(0, len(text) - width):
        yield text[i:i+width]


def text_hmm(text: str, width: int) -> Counter:
    hmm = Counter()
    for fragment in text_fragments(text, width):
        hmm[fragment] += 1
    return hmm

