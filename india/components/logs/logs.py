import logging.handlers
from pathlib import Path

from typing import Callable, Optional

from components.config import Config, APPLICATION, VERSION
from components.helpers import get_directory


def add_stream_handler(
    logger: logging.Logger, logging_level: int = logging.INFO
) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging_level)
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def add_rotating_file_handler(
    logger: logging.Logger, reports_directory: Path, logging_level: int = logging.DEBUG
) -> None:
    file_handler = logging.handlers.RotatingFileHandler(
        Path(logs_path(reports_directory), "logs.txt"), maxBytes=1024*32, backupCount=10
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(levelname)s= %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging_level)
    logger.addHandler(file_handler)


def get_logger(
    name: str,
    add_handler: Callable[[logging.Logger], None],
    logging_level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging_level)
    add_handler(logger)
    return logger


def start_logs() -> None:
    log_handler = None
    if Config.LOG_TO_STDOUT == "YES":
        print('STDOUT logging')
        log_handler = lambda logger: add_stream_handler(logger)
    else:
        fs = get_directory(Config.FILESYSTEM)
        logs_txt = get_resource_identifier(fs.logs, 'logs.txt')
        print('Text File logging :', str(logs_txt))
        log_handler = lambda logger: add_rotating_file_handler(
            logger, reports_directory=logs_txt
        )
    identifier = f"{APPLICATION:s}-{VERSION:s}"
    return get_logger(identifier, log_handler)


LOGS = start_logs()
