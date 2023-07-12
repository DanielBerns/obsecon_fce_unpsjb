import logging

from application import create_app, get_websites()

from components.website_agent import bot_run


IDENTIFIER = "run_news_grabber"


def main() -> None:
    websites = get_websites()

    with create_app(IDENTIFIER) as app:
        bot_run(app.fs.news, websites)


if __name__ == "__main__":
    main()
