import logging
from pathlib import Path
from precios_claros_app import create_app
from pc_scraper import PreciosClarosScraper
from hotel_scraper import HotelScraper

from sampler import Sampler
from context import components
from components.core import SampledDataset

points_of_sale_selection_patterns = [
    {'provincia': 'ar-z', 'localidad': 'caleta olivia'},
    {'provincia': 'ar-z', 'localidad': 'rio gallegos'},
    {'provincia': 'ar-u', 'localidad': 'comodoro rivadavia'},
    {'provincia': 'ar-u', 'localidad': 'rada tilly'},
    {'provincia': 'ar-u', 'localidad': 'trelew'},
    {'provincia': 'ar-u', 'localidad': 'esquel'},
    {'provincia': 'ar-u', 'localidad': 'puerto madryn'},
    {'provincia': 'ar-u', 'localidad': 'rawson'},
]

def filename() -> str:
    return __file__[:-3]

def run(scraper: PreciosClarosScraper) -> None:
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("app created!")
        identifier = scraper.run_identifier
        sampler = Sampler(scraper, points_of_sale_selection_patterns)
        downloads = SampledDataset(app.fs.precios_claros)
        sampler.start()
        downloads.start()
        sample_key, sample_path = downloads.create_sample(identifier)
        sampler.write(sample_path)
        downloads.metadata.add(sample_key, "written", "done")
        downloads.stop()        
        sampler.stop()
        logging.info("stop!")        


if __name__ == "__main__":
    home = Path("~/Data/precios_claros/hotel/downloads/202207292244/")
    scraper = HotelScraper(home.expanduser())
    run(scraper)
