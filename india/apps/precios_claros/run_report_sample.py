import logging
from pathlib import Path
import pdb


from context import components
from components.core import SampledDataset

from precios_claros_app import create_app
from sampler import PreciosClarosSample
from report_sample import FullReportSample, SampleCollector


def filename() -> str:
    return __file__[:-3]

def run(dataset_home: Path, 
        identifier: str,
        report_path: Path) -> None:
    storage = SampledDataset(dataset_home)
    storage.start()
    sample_key, sample_path = storage.get_sample(identifier)
    sample = PreciosClarosSample(sample_path)
    sample_collector = SampleCollector()
    full_report_sample = FullReportSample(sample_collector, sample)
    full_report_sample.write_md(report_path, sample_key)
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()        


def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("instance started!")
        identifier = "20230919150532"
        run(app.fs.precios_claros, identifier, app.fs.reports) 
        logging.info("instance stopped!")

if __name__ == "__main__":
    main()
