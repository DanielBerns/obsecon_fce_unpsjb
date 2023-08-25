import logging

from application import create_app, get_websites

# from components.core import 
from components.website_agent import GrabURLSampleTask

IDENTIFIER = "run_news_bot"


def main() -> None:
    websites = get_websites()
    with create_app(IDENTIFIER) as app:
        print("app created!")
        for identifier, urls in websites.items:        
            print(f"  {identifier:s}")
            with create_treestore_driver(app.fs.news, identifier) as driver:
                for an_url in urls:
                    print(f"    {an_url:s}")                    
                    driver.pipeline.add(GrabURLSampleTask(identifier, an_url))
                    driver.create_sample()
                    driver.pipeline.remove(identifier)                

if __name__ == "__main__":
    main()
