import logging.handlers
from pathlib import Path

from typing import Callable, Optional


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
    logger: logging.Logger, 
    logs_txt: Path, 
    logging_level: int = logging.DEBUG
) -> None:
    file_handler = logging.handlers.RotatingFileHandler(
        logs_txt, maxBytes=1024*32, backupCount=10
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


def get_stdout_logger(identifier: str)  -> logging.Logger:
    log_handler = lambda logger: add_stream_handler(logger)    
    return get_logger(identifier, log_handler)


def get_file_logger(identifier: str, log_txt: str)  -> logging.Logger:
    log_handler = lambda logger: add_rotating_file_handler(
            logger, logs_txt
        )
    return get_logger(identifier, log_handler)
