import logging
import logging.handlers
import sys
from pathlib import Path


def add_stdout_handler(
    logger: logging.Logger, 
    logging_level: int = logging.INFO
) -> None:
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging_level)
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)


def add_file_handler(
    logger: logging.Logger, 
    logs_txt: Path, 
    logging_level: int = logging.DEBUG
) -> None:
    file_handler = logging.handlers.RotatingFileHandler(
        logs_txt, maxBytes=1024*32, backupCount=10
    )
    log_format = "%(asctime)s - %(levelname)s= %(message)s [in %(pathname)s:%(lineno)d]"
    formatter = logging.Formatter(log_format)    
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)
    logger.addHandler(file_handler)

