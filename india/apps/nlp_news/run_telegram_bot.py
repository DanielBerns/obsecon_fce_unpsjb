from context import components
from components.core import CLIConfig
from components.telegram_agent import run

from nlp_news_app import create_app


def filename():
    return __file__[:-3]


def main():
    cli_cfg = CLIConfig()
    with create_app("observatorio_fce_unpsjb", "india", filename(), cli_cfg) as app:
        print("app created!")
        run(app.fs.telegram,
            app.cfg.authorization_token["telegram"],
            app.fs.update_app_sh
        )
        print("The end!")

if __name__ == "__main__":
    main()
