import logging
from pathlib import Path

import pdb

from components.precios_claros.pc_scraper import PreciosClarosScraper

# from components.precios_claros.local_scraper import LocalScraper

from components.core.application import create_application
from components.configuration import CLI
from components.helpers import show, get_container, get_directory

def filename() -> str:
    return __file__[:-3]

from components.precios_claros.sampler import (
    PreciosClarosSampleBuilder,
    create_sample_with_web_content,
    create_sample_with_local_content,
)
from components.core.flatstore import FlatStore

from typing import Dict


def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]


def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"


def execute(home: Path, sample_builder: PreciosClarosSampleBuilder) -> None:
    sample_key = sample_builder.run_identifier
    storage = FlatStore(home, "samples")
    storage.start()
    sample_path = storage.create_sample(sample_key)
    sample_builder.write(sample_path)
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()




def download(precios_claros: Path) -> None:
    selection_patterns = [
        {"provincia": "ar-z", "localidad": "caleta olivia"},
        {"provincia": "ar-z", "localidad": "rio gallegos"},
        {"provincia": "ar-u", "localidad": "comodoro rivadavia"},
        {"provincia": "ar-u", "localidad": "rada tilly"},
        {"provincia": "ar-u", "localidad": "trelew"},
        {"provincia": "ar-u", "localidad": "esquel"},
        {"provincia": "ar-u", "localidad": "puerto madryn"},
        {"provincia": "ar-u", "localidad": "rawson"},
    ]
    with create_sample_with_web_content(selection_patterns) as sample_builder:
        execute(precios_claros, sample_builder)


def translate(precios_claros: Path) -> None:
    home = Path("~/Data/precios_claros/hotel/downloads/").expanduser()
    for sample_key in LOCAL_FILES:
        try:
            sample_path = Path(home, sample_key)
            with create_sample_with_local_content(sample_path) as sample_builder:
                precios_claros = get_container(
                    application.file_system.storage, "precios_claros"
                )
                execute(precios_claros, sample_builder)
        except Exception as message:
            logging.error(f"sample_key: {sample_key:s}: {str(message):s}")


def run_bot() -> None:
    application_name = get_application_name("webdeprecios")
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
        precios_claros = get_container(
            application.file_system.storage, "precios_claros"
        )
        download(precios_claros)
