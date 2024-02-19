from pathlib import Path
from components.helpers import get_resource
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import PointOfSale, ArticleWithPrices
from components.precios_claros.delta_doc import DeltaDoc
from components.precios_claros.delta_writer import DeltaWriter
    
class PreciosClarosDeltaWriter:
    def __init__(self, resource: Path, delta: DeltaDoc) -> None:
        self._resource = resource        
        self._delta = delta        

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def delta(self) -> DeltaDoc:
        return self._delta

    def start(self) -> None:
        pass

    def header(self, 
               reference: PreciosClarosSample, 
               current: PreciosClarosSample) -> None:
        reference_key = str(reference.sample_key)[:6]
        current_key = str(current.sample_key)[:6]        
        first_row = [
          f"Referencia {reference_key:s} - Medición {current_key:s}",
          "",
          "",
          "",
          ]
        second_row = [
          "Código de artículo - Marca - Nombre de artículo",
          f"Mínimo    ",
          f"Indicativo",
          f"Máximo    ",
          ]
        self.delta.header(first_row, second_row)

    def card(self, 
             ref_awp: ArticleWithPrices, 
             cur_awp: ArticleWithPrices) -> None:
        ref_ps = ref_awp.prices_stats
        cur_ps = cur_awp.prices_stats

        color_k = lambda k: "FFDDDD" if float(ref_ps[k]) < float(cur_ps[k]) else "DDFFDD"
        
        first_row = [
          f"{ref_awp.article.code:s} - {ref_awp.article.brand:s} - {ref_awp.article.name:s}",
          f"{str(ref_ps[0]):s}",
          f"{str(ref_ps[1]):s}",
          f"{str(ref_ps[2]):s}",
          ]
        second_row = [
          ("", "FFFFFF"),
          (f"{str(cur_ps[0]):s}", color_k(0)),
          (f"{str(cur_ps[1]):s}", color_k(1)),
          (f"{str(cur_ps[2]):s}", color_k(2)),
          ]
        self.delta.card(first_row, second_row)
        
    def footer(self) -> None:
        self.delta.footer()

    def stop(self) -> None:
        self.delta.write(self.resource)


def build_delta_writer(
    home: Path, 
    place: str,
    delta: DeltaDoc
    ) -> DeltaWriter:
    parts = place.split(":")
    name = parts[1].replace(" ", "_")
    resource = Path(home, f"delta_{name:s}")
    return PreciosClarosDeltaWriter(resource, delta)
