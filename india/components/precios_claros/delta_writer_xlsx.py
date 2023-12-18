from typing import Protocol, Tuple
from pathlib import Path
from components.helpers import get_resource
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import (PointOfSale, ArticleWithPrices)
from components.precios_claros.delta_writer import DeltaWriter

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment
import pdb

class DeltaWriterXLSX:
    def __init__(self, resource: Path) -> None:
        self._resource = resource
        wb = Workbook()
        delta = wb.active
        delta.title = "Diferencia de precios"
        delta.column_dimensions['A'].width = 70
        delta.column_dimensions['B'].width = 20
        delta.column_dimensions['C'].width = 20
        delta.column_dimensions['D'].width = 20
        self._workbook = wb
        self._delta = delta
        self._cursor_deltas = 0

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def workbook(self) -> Workbook:
        return self._workbook
    
    @property
    def cursor_deltas(self) -> int:
        return self._cursor_deltas
    
    @cursor_deltas.setter
    def cursor_deltas(self, value: int) -> None:
        self._cursor_deltas = value

    @property
    def delta(self) -> Worksheet:
        return self._delta

    def start(self) -> None:
        pass
    
    def header(self,  
               reference: PreciosClarosSample, 
               current: PreciosClarosSample
               ) -> None:
        self.cursor_deltas = 1
        ak = f'A{self.cursor_deltas:d}'
        bk = f'B{self.cursor_deltas:d}'
        ck = f'C{self.cursor_deltas:d}'
        dk = f'D{self.cursor_deltas:d}'

        ref_key = str(reference.sample_key)[:-6]
        self.delta[ak] = "Código de artículo - Marca"
        self.delta[bk] = f"Mínimo     - {ref_key:s}"
        self.delta[ck] = f"Indicativo - {ref_key:s}"
        self.delta[dk] = f"Máximo     - {ref_key:s}"
        
        self.cursor_deltas += 1
        ak = f'A{self.cursor_deltas:d}'
        bk = f'B{self.cursor_deltas:d}'
        ck = f'C{self.cursor_deltas:d}'
        dk = f'D{self.cursor_deltas:d}'
        
        cur_key = str(current.sample_key)[:-6]
        self.delta[ak] = "Nombre de artículo        "
        self.delta[bk] = f"Mínimo     - {cur_key:s}"
        self.delta[ck] = f"Indicativo - {cur_key:s}"
        self.delta[dk] = f"Máximo     - {cur_key:s}"
        self.cursor_deltas += 1
        
    def line(self, 
             ref_awp: ArticleWithPrices,
             cur_awp: ArticleWithPrices
             ) -> None:
        ref_ps = ref_awp.prices_stats
        cur_ps = cur_awp.prices_stats        
        
        self.cursor_deltas += 1
        ak = f'A{self.cursor_deltas:d}'
        bk = f'B{self.cursor_deltas:d}'
        ck = f'C{self.cursor_deltas:d}'
        dk = f'D{self.cursor_deltas:d}'
        
        self.delta[ak] = f"{ref_awp.article.code:s} - {ref_awp.article.brand:s}"
        self.delta[bk] = f"{str(ref_ps[0]):s}"
        self.delta[ck] = f"{str(ref_ps[1]):s}"
        self.delta[dk] = f"{str(ref_ps[2]):s}"

        self.cursor_deltas += 1
        ak = f'A{self.cursor_deltas:d}'
        bk = f'B{self.cursor_deltas:d}'
        ck = f'C{self.cursor_deltas:d}'
        dk = f'D{self.cursor_deltas:d}'

        self.delta[ak] = f">>  {ref_awp.article.name:s}"
        self.delta[bk] = f"{str(cur_ps[0]):s}"
        self.delta[ck] = f"{str(cur_ps[1]):s}"
        self.delta[dk] = f"{str(cur_ps[2]):s}"
        
        self.cursor_deltas += 1

    def footer(self) -> None:
        pass    
        
    def stop(self) -> None:
        # pdb.set_trace()
        self.workbook.save(self.resource)
 
def build_delta_writer_xlsx(home: Path, place: str) -> DeltaWriter:
    parts = place.split(':')
    name = parts[1].replace(' ', '_')
    resource = get_resource(home, 
                            f"delta_{name:s}",
                            ".xlsx")
    return DeltaWriterXLSX(resource)
