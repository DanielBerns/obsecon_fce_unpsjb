import logging
import math
from collections import Counter, defaultdict
from typing import Tuple, Callable, List, Dict
from components.nlp.tokenizer import Tokenizer
from components.helpers import classname


StringMapping = Tuple[Callable[[str], List[int]], Callable[[List[int]], str]]


class IDFNode:
    def __init__(self) -> None:
        self._number_of_docs = 0
        self._terms = defaultdict(list)
        
    @property
    def number_of_docs(self) -> int:
        return self._number_of_docs

    @number_of_docs.setter
    def number_of_docs(self, value: int) -> None:
        self._number_of_docs = value

    @property
    def terms(self) -> List[List[int]]:
        return self._terms
    
    def add(self, encoded_doc: List[int]) -> None:
        cursor = self.number_of_docs
        self.number_of_docs += 1
        for cc in encoded_doc:
            self.terms[cc].append(cursor)

    @property
    def idf(self) -> Dict[int, float]:
        number_of_docs = self.number_of_docs + 1
        return {nn: math.log((number_of_docs / (1 + len(set(tt))))) for nn, tt in self.terms.items()}


class TFNode:
    def __init__(self, tokens: Dict[str, int]) -> None:
        sorted_tokens = sorted(
            ((value, key) for key, value in tokens.items()),
            reverse=True)        
        stoi = { ss:i for i, ss in enumerate((ss for ff, ss in sorted_tokens)) }
        itos = { i:ss for i, ss in enumerate((ss for ff, ss in sorted_tokens)) }
        self._sorted_tokens = sorted_tokens
        sum_ff = sum((ff for ff, ss in sorted_tokens))        
        self._tf = {i:(ff / sum_ff) for i, (ff, ss) in enumerate(sorted_tokens)}
        # encoder: take a string, output a list of integers
        self._encode = lambda s: [stoi[c] for c in s] 
        # decoder: take a list of integers, output a string
        self._decode = lambda l: ''.join([itos[i] for i in l]) 
        self._idf_node = IDFNode()

    @property
    def sorted_tokens(self) -> List[Tuple[int, str]]:
        return self._sorted_tokens

    @property
    def tf(self) -> Dict[int, float]:
        return self._tf

    @property
    def idf_node(self) -> IDFNode:
        return self._idf_node

    def encode(self, sentence: List[str]) -> List[int]:
        try:
            code = self._encode(sentence)
        except KeyError:
            logging.debug(f"{classname(self):s}.encode 1: {sentence:s}")
            code = []
        return code

    def decode(self, code: List[int]) -> List[str]:
        try:
            sentence = self._decode(code)
        except KeyError:
            logging.debug(f"{classname(self):s}.decode 1: {str(code):s}")
            sentence = ""
        return sentence
        
    def add(self, sentence: List[str]) -> List[int]:
        code = self.encode(sentence)
        self.idf_node.add(code)
        return code


class TokensNode:
  
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()
        self._characters = Counter()
        self._tokens = Counter()
        
    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer
    
    @property
    def characters(self) -> Counter:
        return self._characters
    
    @property
    def tokens(self) -> Counter:
        return self._tokens

    def update(self, doc: str) -> None:
        self.characters.update(doc)        
        self.tokens.update( (word for word in self.tokenizer.read(doc)) )  
        
    @property
    def tf_node(self) -> TFNode:
        return TFNode(self.tokens)
