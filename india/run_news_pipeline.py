# run_news_pipeline

from components.website_agent import run_website_pipeline
from application import create_app, get_websites
from components.nlp import create_encoded_text_writer

import pdb

def main() -> None:
    with create_app("run_news_pipeline") as app:
         with create_encoded_text_writer(app.fs.news) as encoded_text_writer:
             websites = get_websites(encoded_text_writer)
             run_website_pipeline(app.fs.news, websites)
    
if __name__ == "__main__":
    main()
