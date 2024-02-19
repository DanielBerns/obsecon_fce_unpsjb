from typing import Protocol, Tuple
from pathlib import Path
from components.helpers import get_resource
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.models import PointOfSale, ArticleWithPrices
from components.precios_claros.delta_writer import DeltaWriter

from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Alignment


class XLSXDeltaDoc:
    def __init__(self) -> None:
        wb = Workbook()
        delta = wb.active
        delta.title = "Diferencia de precios"
        delta.column_dimensions["A"].width = 70
        delta.column_dimensions["B"].width = 20
        delta.column_dimensions["C"].width = 20
        delta.column_dimensions["D"].width = 20
        self._workbook = wb
        self._delta = delta
        self._cursor_deltas = 0
        ref_key = str(reference.sample_key)[:6]        
        cur_key = str(current.sample_key)[:6]

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
      
    def header(self, 
               first_row: List[str], 
               second_row: List[str]) -> None:

        self.cursor_deltas = 1
        cursors = [f"{letter:s}{self.cursor_deltas:d}"] for letter in "ABCD"]
        for a_cursor, label in zip(cursors, first_row):
            self.delta[cursor] = label

        self.cursor_deltas += 1
        cursors = [f"{letter:s}{self.cursor_deltas:d}"] for letter in "ABCD"]
        for a_cursor, label in zip(cursors, second_row):
            self.delta[cursor] = label

        self.cursor_deltas += 1

    
    def card(self, 
             first_row: List[str], 
             second_row: List[Tuple[str, str]]) -> None:

        self.cursor_deltas += 1
        cursors = [f"{letter:s}{self.cursor_deltas:d}"] for letter in "ABCD"]
        for a_cursor, content in zip(cursors, first_row):
            self.delta[cursor] = content

        self.cursor_deltas += 1
        cursors = [f"{letter:s}{self.cursor_deltas:d}"] for letter in "ABCD"]
    
        for _cursor, (_content, _color) in zip(cursors, second_row):
            cell = self.delta[_cursor]
            cell = _content
            cell.font = cell.font.copy(color=_color)
            
        self.cursor_deltas += 1


    def write(self, resource: Path) -> None:
        self.workbook.save(resource)


