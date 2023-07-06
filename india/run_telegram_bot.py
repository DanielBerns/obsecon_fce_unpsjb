import logging

from application.engine import create_app

from components.telegram_agent import bot_run


IDENTIFIER = "run_telegram_bot"


def main():
    with create_app(IDENTIFIER) as app:
        bot_run(
            app.fs.application_home, 
            app.fs.telegram, 
            app.config.authorization_token["telegram"]
        )


if __name__ == "__main__":
    main()
