import logging
from pathlib import Path

from components.precios_claros.pc_scraper import PreciosClarosScraper
from components.precios_claros.local_scraper import LocalScraper

from components.precios_claros.app import create_app
from components.precios_claros.sampler import (PreciosClarosSampleBuilder, 
                                               create_sample_with_web_content, 
                                               create_sample_with_local_content)
from components.core.flatstore import FlatStore

from typing import Dict


def filename() -> str:
    return __file__[:-3]


def execute(
    home: Path, 
    sample_builder: PreciosClarosSampleBuilder
    ) -> None:
    sample_key = sample_builder.run_identifier
    storage = FlatStore(home, "samples")    
    storage.start()    
    sample_path = storage.create_sample(sample_key)
    sample_builder.write(sample_path)
    storage.metadata.add(sample_key, f"{filename():s}.run", "done")
    storage.stop()        

def run_bot() -> None:
    web = True
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        if web:
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
                execute(app.fs.precios_claros, sample_builder)    
        else:
            pass
            # home = Path("~/Data/precios_claros/hotel/downloads/202207292244/")
            # with create_sample_with_local_content(home) as sample_builder:
            #     execute(app.fs.precios_claros, sample_builder)    
