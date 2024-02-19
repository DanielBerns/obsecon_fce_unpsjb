from collections import Counter
from pathlib import Path
from typing import List, Dict, Generator

from components.nlp.tokenizer import Tokenizer


class TextCode:
    def __init__(self, base: Path) -> None:
        encoded_tokens = TokensMD.read(base)
        encoded_tokens["<Initial>"] = -1
        encoded_tokens["<Final>"] = -2
        decoded_tokens = {v: k for k, v in encoded_tokens.items()}
        self._encoded_tokens = encoded_tokens
        self._decoded_tokens = decoded_tokens
        self._tokenizer: Tokenizer = Tokenizer()

    @property
    def encoded_tokens(self) -> Dict[str, int]:
        return self._encoded_tokens

    @property
    def decoded_tokens(self) -> Dict[int, str]:
        return self._decoded_tokens

    @property
    def tokenizer(self) -> Tokenizer:
        return self._tokenizer

    def encode(self, text_txt: Path) -> Generator[List[int], None, None]:
        try:
            for sentence in TextTXT.read_sentences(text_txt):
                encoded_sentence = [
                    self.encoded_tokens[token]
                    for token in self.tokenizer.read(sentence)
                ]
                yield encoded_sentence
        except Exception as message:
            print("    Error:", str(message))

    def decode(self, encoded_sentence: List[int]) -> List[str]:
        return [self.decoded_tokens[code] for code in encoded_sentence]


class EncodedText:
    @staticmethod
    def serialize(encoded_sentence: List[int]) -> str:
        return "[" + ",".join(str(dd) for dd in encoded_sentence) + "]\n"

    @staticmethod
    def deserialize(line: str) -> List[int]:
        array = line[1:-2]
        parts = array.split(",")
        numbers = [int(pp) for pp in parts]
        yield numbers

    @staticmethod
    def read(encoded_text_jsonl: Path) -> Generator[List[int], None, None]:
        with open(encoded_text_jsonl, "r") as source:
            for line in source:
                yield EncodedText.deserialize(line)

    @staticmethod
    def encode_text(text_txt: Path, encoded_text_jsonl: Path, text_code: TextCode) -> None:
        with open(encoded_text_jsonl, 'w') as target: 
            for encoded_sentence in text_code.encode(text_txt):
                line = EncodedText.serialize(encoded_sentence)
                target.write(f"{line:s}\n")
            
    @staticmethod
    def decode_text(encoded_text_jsonl: Path, text_txt: Path, text_code: TextCode) -> None:
        with open(text_txt, 'w') as target:
            for encoded_sentence in EncodedText.read(encoded_text_jsonl):
                sequence = text_code.decode(encoded_sentence)
                line = ' '.join(sequence)
                target.write(f"{line:s}\n")            
