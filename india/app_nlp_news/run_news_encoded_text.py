# run_news_pipeline

from application import create_app

from context import components
from components.nlp import EncodedText
from components.core import create_treestore_driver

IDENTIFIER = "run_news_encoded_text"

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", IDENTIFIER) as app:
        print("app created!")
        keys = ["adnsur"]
        for a_key in keys:
            print(a_key)
            with create_treestore_driver(app.fs.news, a_key) as driver:
                EncodedText.write(driver.store)
    
if __name__ == "__main__":
    main()
