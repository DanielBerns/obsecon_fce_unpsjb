import logging
from pathlib import Path

from components.core import FlatStore

from components.core.application import create_application
from components.configuration import CLI
from components.helpers import show, get_container, get_directory
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import FullReportSample, SampleCollector


import pdb

def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]

def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"


def execute(
    sample_key: str,
    home: Path, 
    report_path: Path
    ) -> None:
    storage = FlatStore(home, "samples")    
    storage.start()    
    sample_path = storage.get_sample(sample_key)
    sample = PreciosClarosSample(sample_path)
    sample_collector = SampleCollector()
    full_report_sample = FullReportSample(sample_collector)
    try:
        full_report_sample.execute(report_path, sample)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{prefix():s}.execute", "done")
    storage.stop()        


def run_report_sample(sample_key: str) -> None:
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
         default="live", required=False,
         help="how to run? dev, test or live",
    )
    arguments = cli.arguments
    with create_application(application_name, arguments) as application:
        show(f"{application_name:s} 1")
        home = get_directory(Path(
            "~", 
            "Info", 
            "observatorio_fce_unpsjb", 
            "india", 
            "live"))
        precios_claros = get_directory(Path(home, "Storage", "precios_claros"))
        reports = get_directory(Path(home, "Reports"))
        execute(sample_key, precios_claros, reports) 
