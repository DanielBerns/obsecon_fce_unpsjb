from application import create_app

from context import components
from components.telegram_agent import run

IDENTIFIER = "run_telegram_bot"

def main():
    with create_app("observatorio_fce_unpsjb", "india", IDENTIFIER) as app:
        print("app created!")
        run(
            app.fs.application_home,
            app.fs.telegram,
            app.config.authorization_token["telegram"]
        )

if __name__ == "__main__":
    main()
