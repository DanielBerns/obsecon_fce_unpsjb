# import logging
from typing import Dict, Generator, Protocol


class PreciosClarosScraper(Protocol):
    @property
    def run_identifier(self) -> str:
        pass

    def start(self) -> None:
        # logging.info(f"{classname(self):s}.start")
        pass

    def stop(self) -> None:
        # logging.info(f"{classname(self):s}.stop")
        pass

    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        # logging.info(f"{classname(self):s}.points_of_sale")
        yield from []

    def selected_points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        # logging.info(f"{classname(self):s}.selected_points_of_sale")
        yield from []

    def articles_per_point_of_sale(
        self, point_of_sale: Dict[str, str]
    ) -> Generator[Dict[str, str], None, None]:
        # logging.info(f"{classname(self):s}.articles_per_point_of_sale")
        yield from []
