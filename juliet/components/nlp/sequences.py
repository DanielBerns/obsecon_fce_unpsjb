from collections import Counter, defaultdict
from components.nlp import Tokenizer
from typing import Dict, Tuple, Generator, List, TextIO
from pathlib import Path

# "/home/dberns/Info/observatorio_fce_unpsjb/india/live/Reports/precios_claros/20231221191057/token_clusters/comodoro_rivadavia.csv"


def build_text_lines_generator(origin: Path) -> Callable[[], Generator[str, None, None]]:
    def text_lines_generator -> Generator[str, None, None]:
        with open(origin, "r") as content:
            for line in content:
                yield line
    return text_lines_generator

def get_tokens(
    get_text_lines: Callable[[], Generator[str, None, None]],
    tokenizer: Optional[Tokenizer] = None
) -> Tuple[List[str], Dict[str, int]]:
    tokenizer = Tokenizer() if tokenizer is None else tokenizer
    frequencies = Counter()
    for line in get_text_lines():
        name_tokens = tokenizer.read(line)
        for a_token in name_tokens:
            frequencies[a_token] += 1
        sorted_tokens = [key for key in sorted(frequencies.keys())]
        indexed_tokens = {token:index for index, token in enumerate(sorted_tokens)}
    return sorted_tokens, indexed_tokens


def get_tokens_and_indexes(
  origin_name: str, 
  indexed_tokens: Dict[str, int],
  ) -> Generator[Tuple[Tuple[str, ...], Tuple[int, ...]], None, None]:
    tokenizer = Tokenizer(separators=" ")    
    with open(origin_name, "r") as origin:
       for line in origin:
           tokens = tokenizer.read(line)
           indexes = [
               indexed_tokens.get(a_token, -1) 
               for a_token in tokens
           ]
           yield tokens, indexes        


class TrieNode:
    def __init__(self):
        self._children: Dict[int, "TrieNode"] = {}
        self._count: int = 0
        
    @property
    def children(self) -> Dict[int, "TrieNode"]:
        return self._children

    @property
    def count(self) -> int:
        return self._count
    
    @count.setter
    def count(self, value: int) -> None:
        self._count = value


class Trie:
    def __init__(self):
        self._root: TrieNode = TrieNode()

    @property
    def root(self) -> TrieNode:
        return self._root

    def insert(self, sequence: List[int]):
        node = self.root
        for index in sequence:
            node.count += 1
            try:
                node = node.children[index]
            except KeyError:
                node.children[index] = auxiliar = TrieNode()
                node = auxiliar

    def sequences(
        self, 
        node: TrieNode, 
        stack: List[Tuple[int, int, int]]
        ) -> Generator[List[Tuple[int, int, int]], None, None]:
        children = len(node.children)
        count = node.count
        if children == 0 and count == 0:
            yield stack
        for index, child in node.children.items():
            stack.append((children, count, index))
            for new_level in self.sequences(child, stack):
                yield new_level 
            stack.pop()

    def structure(
        self,
        node: TrieNode, 
        stack: List[Tuple[int, int, int]],
        target: TextIO
        ) -> None:
        target.write("  "*len(stack))
        target.write(f"{len(stack):d} - ")
        children = len(node.children)
        count = node.count
        target.write(f"({children:d}-{count:d})\n\n")
        for number, (index, child) in enumerate(node.children.items()):
            stack.append((children, count, index))
            target.write(f"  "*len(stack))
            target.write(f"[{number+1:d} of {children:d}] {index:d}\n")
            self.structure(child, stack, target)
            stack.pop()


def collapse(sequence: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    cursor = len(sequence)
    for ff, ss, tt in sequence[-1::-1]:
        if ff == 1:
            cursor -= 1
        else:
            break
    return sequence[:cursor]


class NLP:
    def __init__(self, 
                 sorted_tokens: List[str], 
                 indexed_tokens: Dict[str, int],
                 tokens_trie: Trie) -> None:
        self._sorted_tokens: List[str] = sorted_tokens
        self._indexed_tokens: Dict[str, str] = indexed_tokens
        self._tokens_trie: Trie = tokens_trie
        
    @property
    def sorted_tokens(self) -> List[str]:
        return self._sorted_tokens
    
    @property
    def indexed_tokens(self) -> Dict[str, int]:
        return self._indexed_tokens

    @property
    def tokens_trie(self) -> Trie:
        return self._tokens_trie

    def show(self, sequence: List[Tuple[int, int, int]]) -> str:
        return " ".join([
            f"({children:d}|{count:d}|{self.sorted_tokens[index]:s})" 
            for children, count, index in sequence])
    
    def traverse(self) -> Generator[List[Tuple[int, int, int]], None, None]:
        for current in self.tokens_trie.sequences(self.tokens_trie.root, []):
            yield current

    def collapsed_sequences(self) -> Generator[List[Tuple[int, int, int]], None, None]:
        for sequence in self.traverse():
            yield collapse(sequence)
            
            
    def line(self, sequence: List[Tuple[int, int, int]]) -> str:
        return " ".join(self.sorted_tokens[index] for children, count, index in sequence)
            
    def process(
        self,
        max_length: int = 2
        ) -> Tuple[Counter, DefaultDict[List[str]]]:

        sequence_counter = Counter()
        sequence_map = defaultdict(list)
        for sequence in self.traverse():
            shortened = sequence[:max_length]
            key = self.line(shortened)
            sequence_counter[key] += 1
            sequence_map[key].append(self.line(sequence))
        return sequence_counter, sequence_map
        
    def tree_of_html_pages(
        self, 
        target_container: Path,
        sequence_counter: Counter,
        sequence_map: DefaultDict[List[str]]
    ) -> None:
        root_name = Path(target_container, "root.html") 
        with open(root_name, "w") as root:
            root.write('<html>\n')
            root.write('<head>\n')
            root.write('</head>\n')            
            root.write('<body>\n')
            root.write('<ul>\n')
            for number, (key, value) in enumerate(sequence_counter.items()):
                first, second = number // 256, number % 256
                child = Path(parent, f"{first:>03d}", f"{second:>03d}")
                child.mkdir(mode=0o700, parents=True, exist_ok=True)
                root.write(f'<li><a href="{str(child):s}/child.html">{key:s}</a></li>\n')
                target_child = Path(child, "child.html")
                with open(target_child, 'w') as child:
                    child.write('<html>\n')
                    child.write('<head>\n')
                    child.write('</head>\n')            
                    child.write('<body>\n')
                    child.write('<ul>\n')
                    for name in sequence_map[key]:
                        child.write(f"<li>{name:s}</li>\n")
                    child.write('</ul>\n')
                    child.write('</body>\n')                    
                    child.write('</html>\n')
            root.write('</ul>\n')
            root.write('</body>\n')                    
            root.write('</html>\n')
            
        display_name = Path(target_container, "display.txt")
        with open(display_name, "w") as target:
            for sequence in self.collapsed_sequences():
                line = self.line(sequence)
                target.write(line + "\n")


def build_NLP(origin_name: str) -> NLP:
    sorted_tokens, indexed_tokens = get_tokens(origin_name)
    tokens_trie: Trie = Trie()
    for tokens, indexes in get_sequences(origin_name, indexed_tokens):
        tokens_trie.insert(indexes)
    return NLP(sorted_tokens, indexed_tokens, tokens_trie)

def get_nlp(
    origin_name: Path,
    target_container: Path,
    max_length: int = 2
) -> None:
    sorted_tokens, indexed_tokens = get_tokens(origin_name)
    tokens_trie: Trie = Trie()
    for tokens, indexes in get_sequences(origin_name, indexed_tokens):
        tokens_trie.insert(indexes)
    nlp = NLP(sorted_tokens, indexed_tokens, tokens_trie)
    nlp.process(target_container, max_length)
    return nlp
        
    @property
    def origin_container(self) -> Path:
        return self._origin_container

    @property
    def target_container(self) -> Path:
        return self._target_container
    
    def execute() -> None:
        container = Path('.')
        nlp = build_NLP(self.origin_container)
        nlp.process(self.target_container, max_length=2)

