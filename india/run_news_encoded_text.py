# run_news_pipeline

from components.website_agent import run_website_pipeline
from application import create_app, get_websites
from components.nlp import create_encoded_text_writer

def main() -> None:
    websites = get_websites()
    with create_app("run_news_pipeline") as app:
         with create_encoded_text_writer(app.fs.news) as encoded_text_writer:
             for a_website in websites:
                 container = Path(app.fs.news, a_website.identifier, 'target')
                 sample_task = EncodedTextWriterTask(container, encoded_text_writer)
                 run_website_sample_task(sample_task)
    
if __name__ == "__main__":
    main()
