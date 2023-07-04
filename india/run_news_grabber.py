import logging

from app.engine import Engine
from components.website_agent import agent_run


IDENTIFIER = "run_news_grabber"


def main():
    engine = Engine()

    logging.basicConfig(
        filename=engine.get_logs_resource(IDENTIFIER), 
        level=engine.config.log_level)    

    websites = {}
    websites["adnsur"] = ["https://adnsur.com.ar"]
    websites["jornada"] = ["https://www.diariojornada.com.ar/home"]
    websites["cronica"] = ["https://www.diariocronica.com.ar/"]
    websites["elchubut"] = [
        "https://www.elchubut.com.ar/seccion/comodoro-rivadavia",
        "https://www.elchubut.com.ar/seccion/rawson",
        "https://www.elchubut.com.ar/seccion/trelew",
        "https://www.elchubut.com.ar/seccion/puerto-madryn",
        "https://www.elchubut.com.ar/seccion/esquel"]
    websites["infobae"] = ["https://www.infobae.com/"]
    
    logging.info(f"start {IDENTIFIER:s}")
    bot_run(engine.news, websites)
    logging.info(f"stop {IDENTIFIER:s}")
    
if __name__ == "__main__":
    main()
