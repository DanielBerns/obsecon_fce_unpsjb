import logging
from pathlib import Path
from precios_claros_app import create_app
from pc_scraper import PreciosClarosScraper
from hotel_scraper import HotelScraper

from sampler import Sampler
from context import components
from components.core import SampledDataset

import argparse
from typing import Dict

def filename() -> str:
    return __file__[:-3]

import pdb

def main() -> None:
    
    # pdb.set_trace()
    args = {"web": "no"}
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("app created!")
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
            sampler = Sampler.create_sample_from_web(selection_patterns)
        else:
            home = Path("~/Data/precios_claros/hotel/downloads/202207292244/")
            sampler = Sampler.create_sample_from_storage(home)
        downloads = SampledDataset(app.fs.precios_claros)
        sampler.start()
        downloads.start()
        sample_key, sample_path = downloads.create_sample(sampler.scraper.run_identifier)
        sampler.write(sample_path)
        downloads.metadata.add(sample_key, "written", "done")
        downloads.stop()        
        sampler.stop()
        logging.info("stop!")        


if __name__ == "__main__":
    main()
