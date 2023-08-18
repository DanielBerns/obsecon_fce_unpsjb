# run_news_pipeline

from components.website_agent import run_website_pipeline
from application import create_app, get_websites


def main() -> None:
    websites = get_websites()
    with create_app("run_news_pipeline") as app:
        run_website_pipeline(app.fs.news, websites)

    
if __name__ == "__main__":
    main()
