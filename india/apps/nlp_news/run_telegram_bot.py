from application import create_app

from context import components
from components.telegram_agent import run

NAME = "run_telegram_bot"

def main():
    with create_app("observatorio_fce_unpsjb", "india", "test", NAME) as app:
        print("app created!")
        run(
            app.fs.application_home,
            app.fs.telegram,
            app.config.authorization_token["telegram"]
        )
        print("The end!")

if __name__ == "__main__":
    main()
