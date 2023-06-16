import logging

from app.engine import Engine
from components.telegram_agent import processor_run


IDENTIFIER = "run_telegram_processor"


def main():
    engine = Engine()
    logs_txt = engine.get_logs_resource(IDENTIFIER)
    logging.basicConfig(
        filename=logs_txt, 
        level=engine.config.log_level)    
    logging.info(f"start {IDENTIFIER:s}")
    processor_run(engine.telegram, engine.fs.results)
    logging.info(f"stop {IDENTIFIER:s}")
    
if __name__ == '__main__':
    main()
