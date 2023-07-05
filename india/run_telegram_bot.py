import logging

from components.config import Config
from app.engine import AppFileSystem

from components.telegram_agent import bot_run


IDENTIFIER = "run_telegram_bot"


def main():
    config = Config()
    app_fs = AppFileSystem(config)

    logging.basicConfig(
        filename=app_fs.get_logs_resource(IDENTIFIER), 
        level=config.log_level)    


    logging.info(f"start {IDENTIFIER:s}")
    bot_run(app_fs.application_home,
            app_fs.telegram, 
            config.authorization_token["telegram"])
    logging.info(f"stop {IDENTIFIER:s}")

    
if __name__ == '__main__':
    main()
