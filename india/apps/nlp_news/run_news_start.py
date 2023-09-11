

import logging

from application import create_app
from news import get_websites

from context import components
from components.core import create_treestore_driver
from components.website_agent import GrabURLSampleTask

NAME = "run_news_bot"

DEFAULT_COMMANDS = [
    ("~/Info/observatorio_fce_unpsjb/india/test/Commands/run_bots.sh:45 * * * *",
     "run_bots",),
    ("~/Info/observatorio_fce_unpsjb/india/test/update_repo.sh:15 * * * *", 
     "update_repo",),
]

                                                          




def main() -> None:
    websites = get_websites()
    with create_app("observatorio_fce_unpsjb", "india", "test", NAME) as app:
        print("app created!")



























def main():
    with create_app("observatorio_fce_unpsjb", "india", IDENTIFIER) as app:
        logging.info(f"application_home={str(app.fs.application_home):s}")
        logging.info(f"info_home       ={str(app.fs.info_home):s}")
        print(app.fs.application_home)
        print(app.fs.info_home)
        app.fs.create_commands(DEFAULT_COMMANDS)



if __name__ == "__main__":
    main()
