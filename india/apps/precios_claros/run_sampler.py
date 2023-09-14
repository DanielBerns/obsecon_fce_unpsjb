import logging
from precios_claros_app import create_app
from web_scraper import WebScraper
from downloader import Downloader
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

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "precios_claros", filename()) as app:
        logging.info("app created!")
        scraper = WebScraper()
        downloader = Downloader(scraper, points_of_sale_selection_patterns)
        downloads = SampledDataset(app.fs.precios_claros)
        downloader.start()
        downloads.start()
        sample_key, sample_path = downloads.create_sample()
        downloader.write(sample_path)
        downloads.metadata.add(sample_key, "written", "done")
        downloads.stop()        
        downloader.stop()
        logging.info("stop!")        


if __name__ == "__main__":
    main()
