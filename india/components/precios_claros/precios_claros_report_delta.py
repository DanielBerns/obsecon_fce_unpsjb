import logging
from pathlib import Path
from typing import Dict, Tuple

from components.configuration import CLI
from components.core import FlatStore, create_application
from components.helpers import show, get_container, get_timestamp, classname
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.report_delta import DeltaReportSample
from components.precios_claros.delta_writer_xlsx import build_delta_writer_xlsx

import pdb

class PreciosClarosDeltaTask:
    def __init__(
        self,
        reference_key: str,
        current_key: str,
        application_name: str,
        arguments: Dict[str, str],
    ) -> None:
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 1")
            storage_container = get_container(
                application.file_system.storage, "precios_claros"
            )
            storage = FlatStore(storage_container, "samples")
            storage.start()
            reference_container = storage.get_sample(reference_key)
            reference_collector = self.open_reference_collector(reference_container)
            current_container = storage.get_sample(current_key)
            current_collector = self.open_current_collector(current_container)

            show(f"{application_name:s} 2")
            # pdb.set_trace()
            reports_container = get_container(
                application.file_system.reports, "precios_claros"
            )
            delta_key = f"{reference_key:s}-{current_key:s}"
            reports, target_container = self.open_reports(delta_key, reports_container)

            show(f"{application_name:s} 3")
            self.execute(reference_collector, current_collector, target_container)

            show(f"{application_name:s} 4")
            self.close_store(delta_key, storage)
            self.close_store(delta_key, reports)

            show(f"{application_name:s} 5")

    def open_reference_collector(self, reference_container: Path) -> SampleCollector:
        reference_sample = PreciosClarosSample(reference_container)
        reference_collector = SampleCollector(reference_sample)
        return reference_collector

    def open_current_collector(self, current_container: Path) -> SampleCollector:
        current_sample = PreciosClarosSample(current_container)
        current_collector = SampleCollector(current_sample)
        return current_collector

    def open_reports(
        self, delta_key: str, reports_container: Path
    ) -> Tuple[FlatStore, Path]:
        reports = FlatStore(reports_container, "samples")
        reports.start()
        target_container = reports.create_sample(key=delta_key)
        return reports, target_container

    def close_store(self, delta_key: str, store: FlatStore) -> None:
        store.metadata.add(delta_key, f"{classname(self):s}.execute", get_timestamp())
        store.stop()

    def execute(
        self,
        reference_collector: SampleCollector,
        current_collector: SampleCollector,
        target_container: Path,
    ) -> None:
        pass

def prefix() -> str:
    return Path(__file__[:-3]).parts[-1]

def get_application_name(suffix: str) -> str:
    return f"{prefix():s}_{suffix:s}"

class PreciosClarosReportDelta(PreciosClarosDeltaTask):
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
            "-r",
            "--reference_key",
            type=str,
            default="20231221191057",
            help="reference sample key",
        )
        cli.add_arguments(
            "-c",
            "--current_key",
            type=str,
            default="20231226141145",
            help="current sample key",
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
        arguments: Dict[str, str] = cli.arguments
        reference_key = arguments["reference_key"]
        current_key = arguments["current_key"]
        super().__init__(reference_key, current_key, application_name, arguments)

    def execute(
        self,
        reference_collector: SampleCollector,
        current_collector: SampleCollector,
        target_container: Path,
    ) -> None:
        try:
            delta_report_sample = DeltaReportSample()
            delta_report_sample.execute(
                target_container,
                build_delta_writer_xlsx,
                reference_collector,
                current_collector,
            )
        except Exception as message:
            print(str(message))

def run_report_delta() -> None:
    timestamp = get_timestamp()
    report = PreciosClarosReportDelta(timestamp)
    print(classname(report))
