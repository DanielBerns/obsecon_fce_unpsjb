"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict, List, Tuple
import requests
import json

from components.core import Bot, TreeStore
from components.helpers import get_timestamp, get_resource_identifier


class WebsiteBot(Bot):
    def __init__(self, 
                 home: Path, 
                 name: str) -> None:
        super().__init__(TreeStore(home, name))

    def save_response(self, response: requests.models.Response) -> None:
        if response is None:
            return
        if response.status_code == 200:
            sample = self.store.new_sample()
            page_html = get_resource_identifier(sample, 'page', '.html')
            attributes_json = get_resource_identifier(sample, 'attributes', '.json')            
            with open(page_html, 'w') as target:
                target.write(response.text)
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

    def iterate(self, first: int = 0, top: int= -1):
        for sample in self.store.samples():
            yield sample
            
    def read(self, sample: Path) -> Tuple[str, Dict]:
        page_html = get_resource_identifier(sample, 'page', '.html')
        with open(page_html, 'r') as source:
            html = source.read()
        attributes_json = get_resource_identifier(sample, 'attributes', '.json')
        with open(attributes_json, 'r') as source:
            attributes = json.load(source)
        return html, attributes


def bot_run(home: Path,
            websites: Dict[str, List[str]]
        ) -> None:
    logging.info(f"start run: {str(home):s}")
    for identifier, urls in websites.items():
        logging.info(f"  identifier: {identifier:s}")        
        bot = WebsiteBot(home, identifier)
        bot.store.start()
        for this_url in urls:
            bot.grab(this_url)
        bot.store.stop()
        logging.info(f"  done: {identifier:s}")                
    logging.info(f"done run: {str(home):s}")
    
