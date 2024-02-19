from pathlib import Path
from collections import Counter
from components.sequences import (transform_origin, NLP, build_NLP)

        
base = "~/Info/observatorio_fce_unpsjb/india/live/Reports/precios_claros/20231221191057/token_clusters/"
original = "comodoro_rivadavia.csv"
transformed = "transformed.md"
root = "comodoro_rivadavia"
display = "display.txt"

def main() -> None:
    original_name = str(Path(base, original).expanduser())
    transformed_name = str(Path(base, transformed).expanduser())
    container = str(Path(base, root).expanduser())
    display_name = str(Path(container, display).expanduser())    
    transform_origin(original_name, transformed_name)
    nlp = build_NLP(transformed_name)
    nlp.process(container, display_name, max_length=2)


if __name__ == '__main__':
    main()
