import logging
from pathlib import Path
from typing import Dict, Tuple

from components.helpers import get_container, classname

from components.configuration import CLI
from components.core import FlatStore, create_application
from components.helpers import show, get_container

from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector

# import pdb

class PreciosClarosTask:
    def __init__(
        self,
        application_name: str,
        arguments: Dict[str, str]
    ) -> None:
        with create_application(application_name, arguments) as application:
            show(f"{application_name:s} 1")
            storage_container = get_container(
                application.file_system.storage, "precios_claros"
            )
            sample_key = arguments["sample_key"]
            storage, sample_collector = self.open_storage(
                sample_key, storage_container
            )

            show(f"{application_name:s} 2")
            reports_container = get_container(
                application.file_system.reports, "precios_claros"
            )
            reports = self.open_reports(
                sample_key, reports_container
            )
            show(f"{application_name:s} 3")
            self.execute(sample_collector, reports_container)

            show(f"{application_name:s} 4")
            self.close_store(storage)
            self.close_store(reports)

            show(f"{application_name:s} 5")

    def open_storage(
        self, 
        sample_key: str, 
        storage_container: Path
    ) -> Tuple[FlatStore, SampleCollector]:
        storage = FlatStore(storage_container, "samples")
        storage.start()
        origin_container = storage.get_sample(sample_key)
        sample = PreciosClarosSample(origin_container)
        sample_collector = SampleCollector(sample)
        return storage, sample_collector

    def open_reports(
        self, sample_key: str, reports_container: Path
    ) -> FlatStore:
        reports = FlatStore(reports_container, "samples")
        reports.start()
        return reports

    def close_store(self, sample_key: str, store: FlatStore) -> None:
        store.metadata.add(sample_key, f"{classname(self):s}.execute", get_timestamp())
        store.stop()

    def execute(
        self, sample_collector: SampleCollector, target_container: Path
    ) -> None:
        pass
