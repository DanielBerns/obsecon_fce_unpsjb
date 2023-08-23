# run_news_pipeline

from components.website_agent import run_website_pipeline
from application import create_app, get_websites
from components.nlp import encoded_text_writer


def main() -> None:
    with create_app("run_news_pipeline") as app:
         with encoded_text_writer(app.fs.news) as text_writer:
            websites = get_websites(text_writer)
            run_website_pipeline(app.fs.news, websites)
    
if __name__ == "__main__":
    main()
