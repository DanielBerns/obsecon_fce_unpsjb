from components.core import CLIConfig
from components.telegram_agent import run

from components.nlp_news.nlp_news_app import create_app


def filename():
    return __file__[:-3]


def nlp_news_telegram_bot() -> None:
    cli_cfg = CLIConfig()   
    cli_cfg.add_arguments()
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg.args) as app:
        print("app started!")
        run(app.fs.telegram,
            app.cfg.authorization_token["telegram"],
            app.fs.update_app_sh
        )
        print("app stopped!")

