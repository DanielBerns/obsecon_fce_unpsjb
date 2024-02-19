from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple, Generator, Any


class TextTXT:
    @staticmethod
    def write(text_txt: Path, content: List[List[Any]]) -> None:
        with open(text_txt, "w") as target:
            for row in content:
                for value in row:
                    target.write(f"{str(value):s}\n")

    @staticmethod
    def read(text_txt: Path) -> str:
        with open(text_txt, "r") as source:
            lines = [line[:-1] for line in source if not line.startswith("#")]
            text = "\n".join(lines)
        return text

    @staticmethod
    def read_sentences(text_txt: Path) -> Generator[str, None, None]:
        with open(text_txt, "r") as source:
            for line in source:
                if not line.startswith("#"):
                    yield line


def get_sorted_characters(some_characters: List[str]) -> str:
    return "".join(sorted(some_characters))


class CharactersMD:
    title: str = "# Characters\n"

    @staticmethod
    def write(characters_md: Path, characters: Counter) -> None:
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
    separator: str = "::::"
    title: str = "# Tokens\n"

    @staticmethod
    def write(tokens_md: Path, tokens: Counter) -> None:
        with open(tokens_md, "w") as target:
            target.write(TokensMD.title)
            max_token_length = 0
            for key, value in sorted(
                tokens.items(), key=lambda pair: pair[1], reverse=True
            ):
                target.write(f"{key:<25s}{TokensMD.separator:s}{value:d}\n")
                token_length = len(key)
                if token_length > max_token_length:
                    max_token_length = token_length

    @staticmethod
    def read(tokens_md: Path) -> Dict[str, int]:
        tokens: Dict[str, int] = {}
        with open(tokens_md, "r") as target:
            title = target.readline()
            assert title == TokensMD.title
            for number, line in enumerate(target):
                parts = line.split(TokensMD.separator)
                try:
                    assert len(parts) == 2
                    word = parts[0].strip()
                    tokens[word] = number
                except AssertionError:
                    print(number, line)
        return tokens
