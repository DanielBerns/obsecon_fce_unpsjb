import logging

from application import create_app
from news import get_websites

from context import components
from components.core import create_treestore_driver
from components.website_agent import GrabURLSampleTask

IDENTIFIER = "run_news_bot"

def main() -> None:
    websites = get_websites()
    with create_app("observatorio_fce_unpsjb", "india", IDENTIFIER) as app:
        print("app created!")
        for identifier, urls in websites.items():        
            print(f"  {identifier:s}")
            with create_treestore_driver(app.fs.news, identifier) as driver:
                for an_url in urls:
                    print(f"    {an_url:s}")                    
                    driver.pipeline.add(GrabURLSampleTask(identifier, an_url))
                    driver.create_sample()
                    driver.pipeline.remove(identifier)                
    print("Stop!")
    
if __name__ == "__main__":
    main()
