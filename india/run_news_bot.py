import logging

from application import create_app, get_websites

from components.website_agent import bot_run


IDENTIFIER = "run_news_bot"


def main() -> None:
    websites = get_websites()

    with create_app(IDENTIFIER) as app:
        for a_website in websites:
            run_website_bot(app.fs.news, 
                            website.identifier, 
                            website.url)

if __name__ == "__main__":
    main()
