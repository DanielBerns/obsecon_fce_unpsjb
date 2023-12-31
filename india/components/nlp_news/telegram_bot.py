import logging
from pathlib import Path

from typing import Generator, Tuple, List
from components.core.application import create_application
from components.configuration import CLI
from components.telegram_agent import run_bot
from components.helpers import show, get_container

# import pdb


def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]


def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"


def run_telegram_bot(bot_identifier: str) -> None:
    application_name = get_application_name(bot_identifier)
    cli = CLI()
    cli.add_arguments(
        "-d",
        "--dotenv",
        type=str,
        default=".env",
        help="name of dotenv file",
    )
    cli.add_arguments(
        "-m",
        "--mode",
        choices=["dev", "test", "live"],
        type=str,
        default="live",
        required=False,
        help="how to run? dev, test or live",
    )
    arguments = cli.arguments
    with create_application(application_name, arguments) as application:
        show(f"{application_name:s} 1")
        # pdb.set_trace()
        secrets_home = get_container(application.file_system.secrets, "telegram")
        telegram_home = get_container(application.file_system.storage, "telegram")
        run_bot(secrets_home, telegram_home, bot_identifier)
        show(f"{application_name:s} 2")
    show(f"{application_name:s} 3")
