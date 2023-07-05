import logging

from components.config import Config
from app.engine import AppFileSystem

from components.telegram_agent import processor_run


IDENTIFIER = "run_telegram_processor"


def main():
    config = Config()
    app_fs = AppFileSystem(config)

    logging.basicConfig(
        filename=app_fs.get_logs_resource(IDENTIFIER), 
        level=config.log_level)    

    logging.info(f"start {IDENTIFIER:s}")
    processor_run(app_fs.telegram, app_fs.results)
    logging.info(f"stop {IDENTIFIER:s}")


if __name__ == '__main__':
    main()
