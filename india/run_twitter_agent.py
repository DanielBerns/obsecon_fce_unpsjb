import logging

from app.engine import Engine
from components.twitter_agent import run


IDENTIFIER = "run_twitter_agent"


def main():
    engine = Engine()

    logs_txt = engine.get_logs_resource(IDENTIFIER)
    logging.basicConfig(
        filename=logs_txt, 
        level=engine.config.log_level)    

    logging.info(f"start {IDENTIFIER:s}")
    run(engine.twitter, engine.config.authorization_token["twitter"])
    logging.info(f"stop {IDENTIFIER:s}")    

    
if __name__ == '__main__':
    main()
