from context import components
from components.telegram_agent import run

from nlp_news_app import create_app


def filename():
    return __file__[:-3]

def main():
    with create_app("observatorio_fce_unpsjb", "india", "test", filename) as app:
        print("app created!")
        update_app_sh = get_resource(app.fs.commands, "update_app", ".sh")
        run(app.fs.telegram,
            app.config.authorization_token["telegram"],
            update_app_sh
        )
        print("The end!")

if __name__ == "__main__":
    main()
