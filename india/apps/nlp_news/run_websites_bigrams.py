from pathlib import Path
from collections import Counter

from context import components
from components.nlp import TextCode, TokensMD, NLPContainer, Bigrams
from components.core import create_treestore_driver

from nlp_news_app import create_app


def filename():
    return __file__[:-3]

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "test", filename()) as app:
        print("app created!")
        identifiers = ["adnsur"]
        for an_identifier in identifiers:
            print(an_identifier)
            with create_treestore_driver(app.fs.news, an_identifier) as driver:
                frequency = Bigrams.find_bigrams(driver.store.base)
                Bigrams.write_frequency(driver.store.base, frequency)
                sorted_bigrams = Bigrams.sort_bigrams(frequency)
                Bigrams.write_sorted_bigrams(driver.store.base, sorted_bigrams)                
                                
if __name__ == "__main__":
    main()
