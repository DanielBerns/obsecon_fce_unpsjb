import logging

from typing import Generator, Tuple, List
from components.core.treestore import create_treestore_driver
from components.website_agent import GrabURLSampleTask
from components.nlp_news.app import create_app
from components.nlp_news.websites import get_websites

def filename():
    return __file__[:-3]

def show(message: str) -> None:
    print(message)
    logging.info(message)

def run_websites_bot() -> None:
    def websites_items() -> Generator[Tuple[str, Tuple[str, ...]], None, None]:
        websites = get_websites()
        for identifier, urls in websites.items():        
            show(f"start {identifier:s}")
            yield identifier, urls

    def process_item(identifier: str, urls: Tuple[str, ...]) -> None:
        with create_treestore_driver(app.fs.nlp_news_websites, identifier) as driver:
            for an_url in urls:
                show(f" {an_url:s}")     
                driver.pipeline.add(GrabURLSampleTask(identifier, an_url))
                driver.create_sample()
                driver.pipeline.remove(identifier)                

    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        for identifier, urls in websites_items():
            process_item(identifier, urls)
 
