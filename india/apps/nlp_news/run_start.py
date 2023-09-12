import logging

from context import components
from components.core import Crontab
from components.helpers import get_container, get_resource
from nlp_news_app import create_app

def filename():
    return __file__[:-3]


def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "test", filename()) as app:
        print("app created!")
        crontab = Crontab()
        nlp_news_container = get_container(app.fs.commands, "nlp_news")
        run_bots_sh = get_resource(nlp_news_container, "run_bots", ".sh")
        update_app_sh = get_resource(app.fs.commands, "update_app", ".sh")
        crontab.add("run_bots", 
                    str(run_bots_sh),
                    "45", "*", "*", "*", "*")
        crontab.add("update_app",
                    str(update_app_sh),
                    "15", "*", "*", "*", "*")

        crontab.update(app.fs.crontab_txt)


if __name__ == "__main__":
    main()
