import logging
from typing import Dict, List

from app.engine import Engine

def news_grabber(
    engine: Engine,
    websites: Dict[str, List[str]) -> None:
    news = engine.news
    logging.info(f"news: {str(news):s}")
    for identifier, urls in websites.items():
        logging.info(f"  identifier: {identifier:s}")        
        agent = WebsiteAgent(news, identifier)
        agent.grab_urls(urls)
        logging.info(f"  done: {identifier:s}")                
