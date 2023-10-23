from components.telegram_agent import run

from components.nlp_news.app import create_app


def filename():
    return __file__[:-3]


def run_telegram_bot() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        run(app.fs.nlp_news_telegram,
            app.cfg.authorization_token["telegram"],
            app.fs.update_repo_sh
        )
