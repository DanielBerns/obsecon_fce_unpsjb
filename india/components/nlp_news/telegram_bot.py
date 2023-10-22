from components.telegram_agent import run

from components.nlp_news.app import create_app


def filename():
    return __file__[:-3]


def run_telegram_bot() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        print("app started!")
        run(app.fs.telegram,
            app.cfg.authorization_token["telegram"],
            app.fs.update_app_sh
        )
        print("app stopped!")

