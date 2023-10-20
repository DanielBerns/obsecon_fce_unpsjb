from context import components
from components.nlp import EncodedText
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
                EncodedText.write(driver.store)
    
if __name__ == "__main__":
    main()
