import logging

from components.config import Config
from app.engine import AppFileSystem

IDENTIFIER = "start"

DEFAULT_COMMANDS = [
    (
        "~/Apps/observatorio_fce_unpsjb/india/run_news_grabber.sh:36 * * * *",
        "run_news_grabber",
    ),
    ("~/Apps/observatorio_fce_unpsjb/india/update_app.sh:37 * * * *", "update_app"),
]


def main():
    with create_app(IDENTIFIER) as app:
        logging.info(f"application_home={str(app.fs.application_home):s}")
        logging.info(f"info_home       ={str(app.fs.info_home):s}")

        app.fs.create_commands(DEFAULT_COMMANDS)

        logging.warning("THIS IS A TEST")
        logging.error("THIS IS ANOTHER TEST")
        logging.info(f"start {IDENTIFIER:s}")


if __name__ == "__main__":
    main()
