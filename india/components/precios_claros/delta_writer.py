from typing import Protocol, Tuple
from pathlib import Path
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import PointOfSale, ArticleWithPrices


class DeltaWriter(Protocol):
    @property
    def target_home(self) -> Path:
        ...

    def start(self) -> None:
        ...

    def header(
        self, reference: PreciosClarosSample, current: PreciosClarosSample
    ) -> None:
        ...

    def line(self, ref: ArticleWithPrices, cur: ArticleWithPrices) -> None:
        ...

    def footer(self) -> None:
        ...

    def stop(self) -> None:
        ...
