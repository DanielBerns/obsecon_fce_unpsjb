from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Generator

from components.helpers import load_json, get_container


class TextTXT:
    filename: str = "text.txt"

    @staticmethod
    def write(container: Path, content: List[List[str]]) -> None:
        text_txt = Path(container, TextTXT.filename)
        with open(text_txt, "w") as target:
            for event in content:
                for data in event:
                    target.write(str(data) + "\n")

    @staticmethod
    def read(container: Path) -> str:
        text_txt = Path(container, TextTXT.filename)
        with open(text_txt, "r") as source:
            lines = [line[:-1] for line in source if not line.startswith("#")]
            text = "\n".join(lines)
        return text

    @staticmethod
    def read_sentences(container: Path) -> Generator[str, None, None]:
        text_txt = Path(container, TextTXT.filename)
        with open(text_txt, "r") as source:
            for line in source:
                if not line.startswith("#"):
                    yield line


def get_sorted_characters(some_characters: List[str]) -> str:
    return "".join(sorted(some_characters))


class NLPContainer:
    separator: str = "::::"

    @staticmethod
    def get(base: Path) -> Path:
        return get_container(base, "nlp")


class CharactersMD:
    filename: str = "characters.md"
    title: str = "# Characters\n"

    @staticmethod
    def write(base: Path, characters: Counter) -> None:
        container = NLPContainer.get(base)
        characters_md = Path(container, CharactersMD.filename)
        with open(characters_md, "w") as target:
            target.write(CharactersMD.title)
            characters = get_sorted_characters([cc for cc in characters.keys()])
            for key in characters:
                value = characters[key]
                if ord(key) < 32:
                    target.write(f"&{ord(key):>8d}: {value:d}\n")
                elif 32 <= ord(key) < 127:
                    target.write(f">{key:>8s}: {value:d}\n")
                else:
                    target.write(f"&{ord(key):8d}: {value:d}\n")


class TokensMD:
    filename: str = "tokens.md"
    title: str = "# Tokens\n"

    @staticmethod
    def write(base: Path, tokens: Counter) -> None:
        container = NLPContainer.get(base)
        tokens_md = Path(container, TokensMD.filename)
        with open(tokens_md, "w") as target:
            target.write(TokensMD.title)
            max_token_length = 0
            for key, value in sorted(
                tokens.items(), key=lambda pair: pair[1], reverse=True
            ):
                target.write(f"{key:<25s}{NLPContainer.separator:s}{value:d}\n")
                token_length = len(key)
                if token_length > max_token_length:
                    max_token_length = token_length

    @staticmethod
    def read(base: Path) -> Dict[str, int]:
        tokens: Dict[str, int] = dict()
        container = NLPContainer.get(base)
        tokens_md = Path(container, TokensMD.filename)
        with open(tokens_md, "r") as target:
            title = target.readline()
            assert title == TokensMD.title
            for number, line in enumerate(target):
                parts = line.split(NLPContainer.separator)
                try:
                    assert len(parts) == 2
                    word = parts[0].strip()
                    tokens[word] = number
                except AssertionError:
                    print(number, line)
        return tokens
