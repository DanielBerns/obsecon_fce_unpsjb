import logging
from typing import Dict, List

from app.engine import Engine

from components.website_agent import run

def news_grabber(
    engine: Engine,
    websites: Dict[str, List[str]) -> None:
    
    news = engine.news
    logging.info(f"news: {str(news):s}")
    
    run(news, websites)           
