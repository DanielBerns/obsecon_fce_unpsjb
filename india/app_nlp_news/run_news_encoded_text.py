# run_news_pipeline

from application import create_app

from context import components
from components.nlp import EncodedText
from components.core import create_treestore_driver

NAME = "run_news_encoded_text"

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "test", NAME) as app:
        print("app created!")
        identifiers = ["adnsur"]
        for an_identifier in identifiers:
            print(an_identifier)
            with create_treestore_driver(app.fs.news, an_identifier) as driver:
                EncodedText.write(driver.store)
    
if __name__ == "__main__":
    main()
