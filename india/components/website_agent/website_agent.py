"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict, Tuple
import requests
import json

from components.core import Bot, TreeStore
from components.helpers import get_timestamp, get_resource_identifier
from components.website_agent.website import Website

class WebsiteBot(Bot):
    def __init__(self, home: Path, name: str) -> None:
        super().__init__(TreeStore(home, name))

    def save_response(self, response: requests.models.Response) -> None:
        if response is None:
            return
        if response.status_code == 200:
            sample = self.store.new_sample()
            page_html = get_resource_identifier(sample, "page", ".html")
            attributes_json = get_resource_identifier(sample, "attributes", ".json")
            with open(page_html, "w") as target:
                target.write(response.text)
            attributes = {"timestamp": get_timestamp(), "url": response.url}
            with open(attributes_json, "w") as target:
                json.dump(attributes, target)
        else:
            logging.info(f":  status_code: {response.status_code:d}")

    def grab(self, url: str) -> requests.models.Response:
        logging.info(f"start grab({url:s})")
        try:
            response = requests.get(url)
            self.save_response(response)
        except Exception as message:
            logging.info(f":  exception {str(message):s}")
            response = None
        else:
            logging.info(f"done grab({url:s})")
        return response

    def iterate(self, first: int = 0, top: int = -1):
        for sample in self.store.samples():
            yield sample

    def read(self, sample: Path) -> Tuple[str, Dict]:
        page_html = get_resource_identifier(sample, "page", ".html")
        with open(page_html, "r") as source:
            html = source.read()
        attributes_json = get_resource_identifier(sample, "attributes", ".json")
        with open(attributes_json, "r") as source:
            attributes = json.load(source)
        return html, attributes


def run_website_bot(
    bot_home: Path, 
    identifier: str, 
    url: str) -> None:
    logging.info(f"start run: {str(bot_home):s}")
    logging.info(f"  identifier: {identifier:s}")
    bot = WebsiteBot(bot_home, identifier)
    bot.store.start()
    bot.grab(url)
    bot.store.stop()
    logging.info(f"  done: {identifier:s}")
    logging.info(f"done run: {str(bot_home):s}")


def run_website_pipeline(
    bot_home: Path, 
    website: Website) -> None:
    for website in websites:
        bot = WebsiteBot(app.fs.news, website.identifier)
        bot.store.start()
        pipeline = website.pipeline
        dataset_processor = TreeStoreProcessor(bot.store, pipeline)
        dataset_processor.execute()
        bot.store.stop()
