"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict
import requests
import json

from components.core import TreeStore
from components.helpers import get_timestamp


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
            page_html = Path(sample, 'page').with_suffix('.html')
            with open(page_html, 'w') as target:
                target.write(response.text)
            attributes_json = Path(sample, 'attributes').with_suffix('.json')
            attributes = {'timestamp': get_timestamp(), 'url': url}
            with open(attributes_json, 'w') as target:
                json.dump(attributes, target)
        else:
            logging.info(f':  status_code: {response.status_code:d}')

    def get_one_url(self, url: str):
        logging.info(f'start get({url:s})')
        try:
            response = requests.get(url)
        except Exception as message:
            logging.info(f':  exception {str(message):s}')
            response = None
        else:
            logging.info(f'done get({url:s})')
        return response
    
    def grab_urls(self, urls: List[str]):
        logging.info('start grab_urls')
        for one_url in urls:
            response = self.get_one_url(one_url)
            self.save_response(response)
        logging.info('done grab_urls')
