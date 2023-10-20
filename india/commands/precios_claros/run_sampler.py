import logging
from pathlib import Path
from precios_claros_app import create_app, AppPreciosClaros
from pc_scraper import PreciosClarosScraper
from local_scraper import LocalScraper

from sampler import (PreciosClarosSampleBuilder, 
                     create_sample_with_web_content, 
                     create_sample_with_local_content)
from context import components
from components.core import SampledDataset

from typing import Dict

def filename() -> str:
    return __file__[:-3]

import pdb

def run(dataset_home: Path, sample_builder: PreciosClarosSampleBuilder) -> None:
    storage = SampledDataset(dataset_home)
    storage.start()
    sample_key, sample_path = storage.create_sample(sample_builder.run_identifier)
    sample_builder.write(sample_path)
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()        

def main() -> None:
    args = {"web": "yes"}
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("app started!")
        if args["web"] == "yes":
            selection_patterns = [
                {'provincia': 'ar-z', 'localidad': 'caleta olivia'},
                {'provincia': 'ar-z', 'localidad': 'rio gallegos'},
                {'provincia': 'ar-u', 'localidad': 'comodoro rivadavia'},
                {'provincia': 'ar-u', 'localidad': 'rada tilly'},
                {'provincia': 'ar-u', 'localidad': 'trelew'},
                {'provincia': 'ar-u', 'localidad': 'esquel'},
                {'provincia': 'ar-u', 'localidad': 'puerto madryn'},
                {'provincia': 'ar-u', 'localidad': 'rawson'},
            ]            
            with create_sample_with_web_content(selection_patterns) as sample_builder:
                run(app.fs.precios_claros, sample_builder)    
        else:
            home = Path("~/Data/precios_claros/hotel/downloads/202207292244/")
            with create_sample_with_local_content(home) as sample_builder:
                run(app.fs.precios_claros, sample_builder)    
        logging.info("app stopped!")

if __name__ == "__main__":
    main()
