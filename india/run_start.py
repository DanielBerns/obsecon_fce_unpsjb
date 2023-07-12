import logging

from components.config import Config
from app.engine import AppFileSystem

IDENTIFIER = "run_start"

DEFAULT_COMMANDS = [
    (
        "~/Apps/observatorio_fce_unpsjb/india/run_news_bot.sh:36 * * * *",
        "run_news_bot",
    ),
    ("~/Apps/observatorio_fce_unpsjb/india/update_app.sh:37 * * * *", "update_app"),
]


def main():
    with create_app(IDENTIFIER) as app:
        logging.info(f"application_home={str(app.fs.application_home):s}")
        logging.info(f"info_home       ={str(app.fs.info_home):s}")
        app.fs.create_commands(DEFAULT_COMMANDS)



if __name__ == "__main__":
    main()
