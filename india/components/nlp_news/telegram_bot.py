import logging
from pathlib import Path

from typing import Generator, Tuple, List
from components.core.application import create_application
from components.core.config import CLIConfig, build_cli_config
from components.telegram_agent import run_bot
from components.helpers import show, get_container


def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]

def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"

    
def run_telegram_bot(
    bot_identifier: str
    ) -> None:
    cli_config = build_cli_config()
    args = cli_config.args
    mode = args["mode"]
    dotenv = args["dotenv"]
    application_name = get_application_name(bot_identifier)
    with create_application("observatorio_fce_unpsjb", "india", application_name, mode, dotenv) as app:
        show(f"{application_name:s} 1")     
        secrets_home = get_container(app.fs.secrets, "telegram")
        info_home = get_container(app.fs.storage, "telegram")
        run_bot(secrets_home, info_home, bot_identifier)
        show(f"{application_name:s} 2")
    show(f"{application_name:s} 3")
    
