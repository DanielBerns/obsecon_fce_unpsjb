import logging
from pathlib import Path

from components.core import FlatStore

from components.precios_claros.app import create_app
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.report_delta import DeltaReportSample


def filename() -> str:
    return __file__[:-3]


def execute(
    reference_key: str,
    current_key: str,
    home: Path, 
    report_path: Path
    ) -> None:
    storage = FlatStore(home, "samples")    
    storage.start()    
    reference_path = storage.get_sample(reference_key)
    current_path = storage.get_sample(current_key)    
    reference_sample = PreciosClarosSample(reference_path)
    current_sample = PreciosClarosSample(current_path)    
    try:
        delta_report_sample = DeltaReportSample()
        delta_report_sample.execute(report_path, reference_sample, current_sample)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.execute", "done")
    storage.stop()        


def run_report_delta(reference_key: str, current_key: str) -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        execute(reference_key, current_key, app.fs.precios_claros, app.fs.reports) 
