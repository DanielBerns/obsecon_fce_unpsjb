import logging
from pathlib import Path
from typing import Dict, List

from components.website_agent import WebsiteAgent

def run(
    home: Path,
    websites: Dict[str, List[str]) -> None:
    logging.info(f"grab_urls home: {str(home):s}")
    for identifier, urls in websites.items():
        logging.info(f"  identifier: {identifier:s}")        
        agent = WebsiteAgent(home, identifier)
        agent.grab_urls(urls)
        logging.info(f"  done: {identifier:s}")                
 
