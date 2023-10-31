import logging
from pathlib import Path

from components.core import FlatStore

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import FullReportSample, SampleCollector

import pdb

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
    full_report_sample = FullReportSample(sample_collector, sample)
    try:
        full_report_sample.execute(report_path, sample_key)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()        


def run_report_sample() -> None:
    print("hello")
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        sample_key = "20231030184751"
        pdb.set_trace()
        execute(sample_key, app.fs.precios_claros, app.fs.reports) 
