import logging
from pathlib import Path

from components.core import FlatStore

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.report_prefixes import PrefixesReportSample


def filename() -> str:
    return __file__[:-3]

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
    report_sample = PrefixesReportSample(sample_collector, sample)
    try:
        report_sample.execute(report_path, sample_key)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.execute", "done")
    storage.stop()        


def run_report_prefixes() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        sample_key = "20231030184751"
        execute(sample_key, app.fs.precios_claros, app.fs.reports) 
