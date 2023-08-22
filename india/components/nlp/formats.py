class NewsSample:
    page_html = 'page.html'
    attributes_json = 'attributes.json'
    
    @staticmethod
    def read(sample: Path) -> Tuple[str, Dict[str, str]]:
        html = read_text(Path(sample, NewsSample.page_html))
        attributes = load_json(Path(sample, NewsSample.attributes_json))
        return html, attributes


class TextTXT:
    filename: str = 'text.txt'
    
    @staticmethod
    def write(container: Path,
              content: List[str]) -> None:
        text_txt = Path(container, TextTXT.filename)
        with open(text_txt, 'w') as target:
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


def get_sorted_characters(some_characters: List[str]) -> str:
   return "".join(sorted(some_characters))

class CharactersMD:
    filename: str = "characters.md"
    title: str = "# Characters\n"
    
    @staticmethod
    def write(container: Path, 
              store_characters: Counter) -> None:
        characters_md = Path(container, CharactersMD.filename)
        with open(characters_md, "w") as target:
            target.write(CharactersMD.title)
            characters = get_sorted_characters(
                [cc for cc in store_characters.keys()])
            for key in characters:
                value = store_characters[key]
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
    def write(container: Path,
              store_tokens: Counter) -> None:
        tokens_md = Path(container, TokensMD.filename)
        with open(tokens_md, "w") as target:        
            target.write(TokensMD.title)
            max_token_length = 0
            for key, value in sorted(store_tokens.items(), 
                                     key=lambda pair: pair[1],
                                     reverse=True):
                target.write(f"{key:<25s}: {value:d}\n")
                if len(key) > max_token_length:
                    max_token_length = len(key)
                    
    @staticmethod
    def read(container: Path) -> Dict[str, int]:
        tokens: Dict[str, int] = dict()
        tokens_md = Path(container, TokensMD.filename)
        with open(tokens_md, "r") as target:
            title = target.readline()
            assert title == TokensMD.title
            for number, line in enumerate(target):
                parts = line.split(":")
                assert len(parts) == 2
                word = parts[0].strip()
                tokens[word] = number
        return tokens
 
