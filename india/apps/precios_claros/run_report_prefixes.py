import logging
from pathlib import Path

from context import components
from components.core import SampledDataset

from precios_claros_app import create_app
from sampler import PreciosClarosSample
from report_sampler import SampleCollector
from report_prefixes import PrefixesReportSample
from writers import writer_with_target_format

def filename() -> str:
    return __file__[:-3]

import pdb

def run(dataset_home: Path, 
        identifier: str,
        report_path: Path) -> None:
    storage = SampledDataset(dataset_home)
    storage.start()
    sample_key, sample_path = storage.get_sample(identifier)
    sample = PreciosClarosSample(sample_path)
    sample_collector = SampleCollector()
    report_sample = PrefixesReportSample(sample_collector, sample)
    try:
        report_sample.execute(report_path, sample_key)
    except Exception as message:
        print(str(message))
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()        


def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("instance started!")
        identifier = "20230925163551"
        run(app.fs.precios_claros, identifier, app.fs.reports) 
        logging.info("instance stopped!")


if __name__ == "__main__":
    main()
