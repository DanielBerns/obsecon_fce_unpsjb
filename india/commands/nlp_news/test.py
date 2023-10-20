import logging
from pathlib import Path

from context import components
from components.nlp import TokensNode

import pdb

def filename():
    return __file__[:-3]

def main() -> None:
    tokens_node = TokensNode()
    names = ["1998-0", "4300-0", "5200-0", "30254-0", "pg11", 
             "pg2641", "pg6130", "pg7256", "pg27827"]
    
    for a_name in names:    
        resource = Path("~","Data", "mynlp", a_name).with_suffix(".txt").expanduser()
        with open(resource, "r") as origin:
            text = origin.read()
            tokens_node.update(text)

    tf_node = tokens_node.tf_node
    for a_name in names:    
        resource = Path("~","Data", "mynlp", a_name).with_suffix(".txt").expanduser()
        with open(resource, "r") as origin:
            text = origin.read()
            tf_node.add((tt for tt in tokens_node.tokenizer.read(text)))

    tf  = tf_node.tf
    idf = tf_node.idf_node.idf
    
    tfidf = {number:(tf.get(number, 0.0) * idf.get(number, 0.0)) 
             for number, (value, key) in enumerate(tf_node.sorted_tokens)}
    
    sorted_tfidf = sorted(((value, number) for number, value in tfidf.items()), reverse=True)
    
    nlp_output = Path("~","Data", "mynlp", "nlp").with_suffix(".txt").expanduser()    
    with open(nlp_output, 'w') as target:
        for value, key in sorted_tfidf:
            ff, tt = tf_node.sorted_tokens[key]
            target.write(f"{key:>6d} - {tt:>30s}  {tf[key]:>3.12f} {idf[key]:>3.12f} {value:>3.12f}\n")


if __name__ == "__main__":
    main()

