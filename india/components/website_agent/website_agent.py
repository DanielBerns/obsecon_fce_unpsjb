"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict, List
import requests
import json

from components.core import TreeStore
from components.helpers import get_timestamp, get_resource_identifier


class WebsiteAgent:
    def __init__(self, 
                 home: Path, 
                 name: str) -> None:
        self._store = TreeStore(home, name)

    @property
    def store(self):
        return self._store

    def save_response(self, response: requests.models.Response) -> None:
        if response is None:
            return
        if response.status_code == 200:
            sample = self.store.new_sample()
            page_html = get_resource_identifier(sample, 'page', '.html')
            with open(page_html, 'w') as target:
                target.write(response.text)
            attributes_json = get_resource_identifier(sample, 'attributes', '.json')
            attributes = {'timestamp': get_timestamp(), 
                          'url': response.url}
            with open(attributes_json, 'w') as target:
                json.dump(attributes, target)
        else:
            logging.info(f':  status_code: {response.status_code:d}')

    def grab(self, url: str) -> None:
        logging.info(f'start grab({url:s})')
        try:
            response = requests.get(url)
            self.save_response(response)            
        except Exception as message:
            logging.info(f':  exception {str(message):s}')
            response = None
        else:
            logging.info(f'done grab({url:s})')
        return response

def run(home: Path,
        websites: Dict[str, List[str]]
        ) -> None:
    logging.info(f"start run: {str(home):s}")
    for identifier, urls in websites.items():
        logging.info(f"  identifier: {identifier:s}")        
        agent = WebsiteAgent(home, identifier)
        for this_url in urls:
            agent.grab(this_url)
        logging.info(f"  done: {identifier:s}")                
    logging.info(f"done run: {str(home):s}")
