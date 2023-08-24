"""
Bot to access websites 


"""
import logging
from pathlib import Path
from typing import Dict, Tuple, List
import requests
import json

from components.core import TreeStore, TreeStoreProcessor
from components.helpers import get_timestamp, get_resource_identifier
from components.website_agent.website import Website


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
    websites: List[Website]) -> None:
    for website in websites:
        bot = WebsiteBot(bot_home, website.identifier)
        for segment in website.pipeline:
            if segment:
                bot.store.start()
                dataset_processor = TreeStoreProcessor(bot.store, segment)
                dataset_processor.execute()
                bot.store.stop()


    def save_response(self, 
                      url: str,
                      text: str, 
                      code: int, 
                      attributes: Dict[str, str]) -> None:
        logging.info(f"saving response from url{url:s} with code: {code:d}")        
        if text and attributes:
            sample = self.store.new_sample()
            page_html = get_resource_identifier(sample, "page", ".html")
            attributes_json = get_resource_identifier(sample, "attributes", ".json")
            with open(page_html, "w") as target:
                target.write(response.text)
            with open(attributes_json, "w") as target:
                json.dump(attributes, target)
        else:
            logging.info("WebsiteBot.save_response: empty text or attributes")

    def grab(self, url: str) -> Tuple[str, int, Dict[str, str]]:
        logging.info(f"start grab({url:s})")
        html, code, attributes = '', 0, None
        try:
            response = requests.get(url)
            if response is None:
                return '', 0, None
            html, code = response.text, response_status_code
            attributes = {"timestamp": get_timestamp(), 
                          "original url": url,
                          "response.url": response.url}
            self.save_response(url, html, code, attributes)
        except Exception as message:
            logging.info(f"    error grabbing url: {response.url}")
            logging.info(f"    -----> {str(message):s}")            
        logging.info(f"    {url:s} with code {code:d}")
        logging.info(f"done grab({url:s})")
        return html, code, attributes

    def read(self, sample: Path) -> Tuple[str, Dict[str, str]]:
        page_html = get_resource_identifier(sample, "page", ".html")
        with open(page_html, "r") as source:
            html = source.read()
        attributes_json = get_resource_identifier(sample, "attributes", ".json")
        with open(attributes_json, "r") as source:
            attributes = json.load(source)
        return html, attributes
