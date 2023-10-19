import logging

from context import components
from components.core import Crontab
from nlp_news_app import create_app


def filename():
    return __file__[:-3]


def main() -> None:
    cli_cfg = CLIConfig()    
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg) as app:
        print("app created!")
        crontab = Crontab()
        crontab.add("run_bots", 
                    str(app.fs.run_news_bots_sh),
                    "58", "*", "*", "*", "*")
        crontab.add("update_app",
                    str(app.fs.update_app_sh),
                    "15", "*", "*", "*", "*")
        crontab.update(app.fs.crontab_txt)


if __name__ == "__main__":
    main()
