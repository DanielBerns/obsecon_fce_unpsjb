"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict, Tuple
import requests
import json

from components.core import SampleTask
from components.helpers import get_timestamp, get_resource

class GrabURLSample:
          
    @staticmethod
    def grab(url: str) -> Tuple[str, Dict[str, str]]:
        logging.info(f"start grab({url:s})")
        html, http_code, attributes = "", -1, None
        try:
            response = requests.get(url)
            html, http_code = response.text, response.status_code
            attributes = {"timestamp": get_timestamp(), 
                          "original url": url,
                          "response.url": response.url,
                          "http_code": str(http_code)}
        except Exception as message:
            logging.info(f"    error grabbing url: {response.url}")
            logging.info(f"    -----> {str(message):s}")
            html, http_code = "", -1
            attributes = {'error': str(message), 'http_code': http_code}
        else:
            logging.info(f"    {url:s} with http_code {http_code:d}")
        logging.info(f"done grab({url:s})")
        return html, attributes

    @staticmethod
    def read(sample: Path) -> Tuple[str, Dict[str, str]]:
        page_html = get_resource(sample, "page", ".html")
        with open(page_html, "r") as source:
            html = source.read()
        attributes_json = get_resource(sample, "attributes", ".json")
        with open(attributes_json, "r") as source:
            attributes = json.load(source)
        return html, attributes

    @staticmethod
    def write(sample: Path, html: str, attributes: Dict[str, str]):
        page_html = get_resource(sample, "page", ".html")
        with open(page_html, "w") as target:
            target.write(html)
        attributes_json = get_resource(sample, "attributes", ".json")
        with open(attributes_json, "w") as source:
            json.dump(attributes, source)

    @staticmethod
    def execute(sample: Path, url: str) -> None:
        html, attributes = GrabURLSample.grab(url)
        GrabURLSample.write(sample, html, attributes)


class GrabURLSampleTask(SampleTask):
    def __init__(self, identifier: str, url: str) -> None:
        super().__init__(identifier)
        self._url = url
    
    @property
    def url(self) -> None:
        return self._url
    
    def execute(self, sample: Path) -> None:
        GrabURLSample.execute(sample, self.url)
