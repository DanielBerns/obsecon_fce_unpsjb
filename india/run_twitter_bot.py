import logging

from application.engine import create_app
from components.twitter_agent import bot_run

IDENTIFIER = "run_twitter_bot"


def main():
    with create_app(IDENTIFIER) as app:
        bot_run(app.fs.twitter, app.config.authorization_token["twitter"])


if __name__ == "__main__":
    main()
