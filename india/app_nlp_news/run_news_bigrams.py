# from components.nlp import BigramGenerator
# from random import randint
# 
# from collections import Counter
# 
# for k in range(10):
#     sentence = [randint(0,10) for v in range(100)]
#     
#     collect = Counter()
#     for item in BigramGenerator.get(sentence):
#         collect[item] += 1
# 
# for k, v in collect.items():
#     print(str(k), v)
# 

from pathlib import Path
from collections import Counter
from application import create_app

from context import components
from components.nlp import TextCode, TokensMD, NLPContainer, Bigrams
from components.core import create_treestore_driver

IDENTIFIER = "run_news_bigrams"

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", IDENTIFIER) as app:
        print("app created!")
        keys = ["adnsur"]
        for a_key in keys:
            print(a_key)
            with create_treestore_driver(app.fs.news, a_key) as driver:
                frequency = Bigrams.find_bigrams(driver.store.base)
                Bigrams.write_frequency(driver.store.base, frequency)
                sorted_bigrams = Bigrams.sort_bigrams(frequency)
                Bigrams.write_sorted_bigrams(driver.store.base, sorted_bigrams)                
                                
if __name__ == "__main__":
    main()
