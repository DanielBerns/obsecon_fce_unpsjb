import logging
from pathlib import Path

import pdb

from components.precios_claros.pc_scraper import PreciosClarosScraper

# from components.precios_claros.local_scraper import LocalScraper

from components.core.application import create_application
from components.configuration import CLI
from components.helpers import show, get_container, get_directory


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


LOCAL_FILES = [
    "202010281836",
    "202011182258",
    "202011192208",
    "202011252305",
    "202011262341",
    "202012022325",
    "202012032338",
    "202012052331",
    "202012081205",
    "202012090841",
    "202012301245",
    "202101012355",
    "202101022230",
    "202101032356",
    "202101042321",
    "202101061629",
    "202102032042",
    "202102152057",
    "202103152311",
    "202103162229",
    "202104142156",
    "202104152243",
    "202105170951",
    "202106162202",
    "202107161021",
    "202108162012",
    "202109161232",
    "202110201621",
    "202111122001",
    "202111151538",
    "202111161923",
    "202111172155",
    "202112160129",
    "202201151944",
    "202202152312",
    "202203152010",
    "202203222220",
    "202203291240",
    "202203291807",
    "202204062049",
    "202204152207",
    "202205152316",
    "202206061505",
    "202206081508",
    "202206151726",
    "202206221752",
    "202206300911",
    "202207021847",
    "202207061957",
    "202207131959",
    "202207151910",
    "202207201924",
    "202207271954",
    "202207292244",
    "202208032157",
    "202208102027",
    "202208152024",
    "202208271905",
    "202209080938",
    "202209121541",
    "202209121641",
    "202209121806",
    "202209151617",
    "202209222210",
    "202210061340",
    "202210122250",
    "202210142231",
    "202210152009",
    "202211022248",
    "202211092035",
    "202211161301",
    "202211301520",
    "202212011734",
    "202212051901",
    "202212152043",
    "202212212018",
    "202212282104",
    "202212311743",
    "202301012237",
    "202301161611",
    "202302012255",
    "202302022244",
    "202302031609",
    "202302151957",
    "202303011635",
    "202303161500",
    "202304011848",
    "202304141705",
    "202304152209",
    "202304272023",
    "202305042328",
    "202305142159",
    "202305142246",
    "202305151926",
    "202306022234",
    "202306052225",
    "202306060900",
    "202306152035",
    "202307141934",
    "202307311945",
    "202308151902",
    "202309011719",
    "202309131738",
    "202309132059",
    "202310232245",
]


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
    cli.add_arguments(
        "-w",
        "--web",
        choices=["yes", "no"],
        type=str,
        default="yes",
        required=False,
        help="Download from web? yes | no",
    )
    arguments = cli.arguments
    with create_application(application_name, arguments) as application:
        show(f"{application_name:s} 1")
        precios_claros = get_container(
            application.file_system.storage, "precios_claros"
        )
        if arguments["web"] == "yes":
            download(precios_claros)
        else:
            translate(precios_claros)
