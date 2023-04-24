"""
Bot to access websites 


"""
from pathlib import Path
from typing import Dict


from components.core import TreeStore


class WebsiteAgent:
    def __init__(self, 
                 home: Path, 
                 name: str) -> None:
        self._store = TreeStore(home, name)

    @property
    def store(self):
        return self._store

    def get(self, url: str):
        logging.info(f'get({url:s})')
        try
            response = requests.get(url)
        except Exception as message:
            logging.info(f':  exception {str(message):s}')
        else:
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
    
