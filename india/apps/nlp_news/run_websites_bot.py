import logging

from nlp_news_app import create_app
from nlp_news_websites import get_websites

from context import components
from components.core import create_treestore_driver
from components.website_agent import GrabURLSampleTask

def filename():
    return __file__[:-3]

def main() -> None:
    websites = get_websites()
    with create_app("observatorio_fce_unpsjb", "india", "test", filename()) as app:
        print("app created!")
        for identifier, urls in websites.items():        
            print(f"  {identifier:s}")
            logging.info(f"start {identifier:s}")
            with create_treestore_driver(app.fs.news, identifier) as driver:
                for an_url in urls:
                    print(f"    {an_url:s}")     
                    logging.info(f"    {an_url:s}")                    
                    driver.pipeline.add(GrabURLSampleTask(identifier, an_url))
                    driver.create_sample()
                    driver.pipeline.remove(identifier)                
            logging.info(f"done {identifier:s}")
        print("stop!")
    
if __name__ == "__main__":
    main()
