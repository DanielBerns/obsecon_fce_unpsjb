# test_extract_news_with_parsel

import logging

from application import create_app, get_websites
from components.core import TextReaderHTMLWithParsel
from components.website_agent import processor_run

IDENTIFIER = "run_news_processor"

import pdb

def main() -> None:
    websites = get_websites()
    with create_app(IDENTIFIER) as app:
        pdb.set_trace()
        processor_run(app.fs.news, websites, app.fs.results, websites)

if __name__ == "__main__":
    main()
