import logging

from application.engine import create_app

from components.website_agent import bot_run


IDENTIFIER = "run_news_grabber"


def main() -> None:
    websites = {}
    websites["adnsur"] = ["https://adnsur.com.ar"]
    websites["jornada"] = ["https://www.diariojornada.com.ar/home"]
    websites["cronica"] = ["https://www.diariocronica.com.ar/"]
    websites["elchubut"] = [
        "https://www.elchubut.com.ar/seccion/comodoro-rivadavia",
        "https://www.elchubut.com.ar/seccion/rawson",
        "https://www.elchubut.com.ar/seccion/trelew",
        "https://www.elchubut.com.ar/seccion/puerto-madryn",
        "https://www.elchubut.com.ar/seccion/esquel",
    ]
    websites["infobae"] = ["https://www.infobae.com/"]

    with create_app(IDENTIFIER) as app:
        bot_run(app.fs.news, websites)


if __name__ == "__main__":
    main()
