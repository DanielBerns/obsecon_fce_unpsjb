# import logging
from typing import Dict, Generator

class PreciosClarosScraper(Protocol):
    def start(self) -> None:
        # logging.info(f"{classname(self):s}.start")
    
    def stop(self) -> None:
        # logging.info(f"{classname(self):s}.stop")

    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        # logging.info(f"{classname(self):s}.points_of_sale")

    def articles_per_point_of_sale(self, 
                                   point_of_sale: Dict[str, str]
                                   ) -> Generator[Dict[str, str], None, None]:
        # logging.info(f"{classname(self):s}.points_of_sale")
