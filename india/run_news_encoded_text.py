# run_news_pipeline

from application import create_app
from components.nlp import EncodedText
from components.core import create_treestore_driver

def main() -> None:
    with create_app("run_news_pipeline") as app:
        print("app created!")
        keys = ["adnsur"]
        for a_key in keys:
            print(a_key)
            with create_treestore_driver(app.fs.news, a_key) as driver:
                EncodedText.write(driver.store)
    
if __name__ == "__main__":
    main()
