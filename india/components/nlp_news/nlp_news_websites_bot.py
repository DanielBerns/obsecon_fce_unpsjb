import logging


from components.core import create_treestore_driver
from components.website_agent import GrabURLSampleTask
from components.nlp_news.nlp_news_app import create_app
from components.nlp_news.nlp_news_websites import get_websites

def filename():
    return __file__[:-3]

def nlp_news_websites_bot() -> None:
    def websites_items() -> Generator[Tuple[str, List[str]], None, None]:
        websites = get_websites()
        for identifier, urls in websites.items():        
            print(f"  {identifier:s}")
            logging.info(f"start {identifier:s}")
            yield identifier, urls

    def process_item(identifier: str, urls: List[str]) -> None:
        with create_treestore_driver(app.fs.news, identifier) as driver:
            for an_url in urls:
                print(f"    {an_url:s}")     
                logging.info(f"    {an_url:s}")                    
                driver.pipeline.add(GrabURLSampleTask(identifier, an_url))
                driver.create_sample()
                driver.pipeline.remove(identifier)                

    cli_cfg = CLIConfig()   
    cli_cfg.add_arguments()
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg.args) as app:
        print("app started!")
        for identifier, urls in websites_items():
            logging.info(f"done {identifier:s}")
            process_item(identifier, urls)
        print("app stopped!")
