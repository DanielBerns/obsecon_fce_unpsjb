from typing import Protocol, Tuple
from pathlib import Path
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import PointOfSale, ArticleWithPrices


class DeltaWriter(Protocol):

    def start(self) -> None:
        ...

    def header(
        self, reference: PreciosClarosSample, current: PreciosClarosSample
    ) -> None:
        ...

    def card(self, ref: ArticleWithPrices, cur: ArticleWithPrices) -> None:
        ...

    def footer(self) -> None:
        ...

    def stop(self) -> None:
        ...
