import logging

from app.engine import Engine
from components.telegram_agent import run


IDENTIFIER = "run_telegram_agent"


def main():
    engine = Engine()

    logs_txt = engine.get_logs_resource(IDENTIFIER)
    logging.basicConfig(
        filename=logs_txt, 
        level=engine.config.log_level)    

    logging.info(f"start {IDENTIFIER:s}")
    run(engine.config.application_home,
        engine.telegram, 
        engine.config.authorization_token["telegram"])
    logging.info(f"stop {IDENTIFIER:s}")
    
if __name__ == '__main__':
    main()
