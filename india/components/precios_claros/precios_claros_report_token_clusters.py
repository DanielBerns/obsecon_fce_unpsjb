import logging
from pathlib import Path
from typing import Dict

from components.configuration import CLI
from components.core import FlatStore, create_application
from components.helpers import show, get_container, get_timestamp, classname

from components.precios_claros.precios_claros_task import PreciosClarosTask
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.report_token_clusters import TokenClustersReportSample


def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]


def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"


class PreciosClarosReportTokenClusters(PreciosClarosTask):
    def __init__(self, identifier: str) -> None:
        application_name = get_application_name(identifier)
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
            "-s",
            "--sample_key",
            type=str,
            default="20231221191057",
            help="current sample key",
        )        
        arguments: Dict[str, str] = cli.arguments
        super().__init__(application_name, arguments)

    def execute(
        self, sample_collector: SampleCollector, target_container: Path
    ) -> None:
        try:
            report = TokenClustersReportSample(sample_collector)
            report.execute(target_container)
        except Exception as message:
            show(str(message))


def run_report_token_clusters() -> None:
    timestamp = get_timestamp()
    report = PreciosClarosReportTokenClusters(timestamp)
    print(classname(report))
