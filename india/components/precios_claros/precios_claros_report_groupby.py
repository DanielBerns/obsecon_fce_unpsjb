import logging
from pathlib import Path

from components.core import FlatStore
from components.helpers import get_container

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.report_groupby import GroupbyReportSample

import pdb

def filename() -> str:
    return __file__[:-3]

def execute(
    sample_key: str,
    storage_home: Path, 
    reports_home: Path
    ) -> None:
    storage = FlatStore(storage_home, "samples")
    reports = FlatStore(reports_home, "samples")
    storage.start()
    reports.start()
    storage_container = storage.get_sample(sample_key)
    sample = PreciosClarosSample(storage_container)
    sample_collector = SampleCollector()
    groupby_report = GroupbyReportSample(sample_collector, sample)
    report_container = reports.create_sample(key=sample_key)
    try:
        groupby_report.execute(report_container)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.execute", "done")
    storage.stop()        


def run_report_groupby(sample_key: str) -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        execute(sample_key, app.fs.precios_claros, app.fs.reports) 
        
