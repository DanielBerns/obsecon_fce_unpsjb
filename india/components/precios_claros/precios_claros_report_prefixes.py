import logging
from pathlib import Path

from components.core import FlatStore
from components.helpers import get_container

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.prefixes_report import SampleCollector
from components.precios_claros.report_prefixes import PrefixesReportSample

import pdb

def filename() -> str:
    return __file__[:-3]

def execute(
    sample_key: str,
    storage_home: Path, 
    report_container: Path
    ) -> None:
    storage = FlatStore(storage_home, "samples")
    reports = FlatStore(reports_home, "samples")
    storage.start()
    reports.start()
    pdb.set_trace()
    storage_container = storage.get_sample(sample_key)
    sample = PreciosClarosSample(storage_container)
    sample_collector = SampleCollector()
    prefixes_report = PrefixesReportSample(sample_collector, sample)
    pdb.set_trace()    
    report_container = reports.get_sample(sample_key)
    # get_container(Path(report_container, sample_key), 'prefixes')
    try:
        prefixes_report.execute(report_container)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.execute", "done")
    storage.stop()        


def run_report_prefixes() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        sample_key = "20231030184751"
        execute(sample_key, app.fs.precios_claros, app.fs.reports) 
