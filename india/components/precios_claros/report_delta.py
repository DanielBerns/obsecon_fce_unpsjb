from collections import defaultdict, Counter
from pathlib import Path
from typing import DefaultDict, List, Generator, Dict, Tuple, Optional, Callable
import math
from os import walk
import logging
from dataclasses import dataclass

from components.helpers import get_resource, get_container, i, classname
from components.precios_claros.sampler import PreciosClarosSample
from components.precios_claros.report_sample import SampleCollector
from components.precios_claros.models import PointOfSale, ArticleWithPrices

from components.precios_claros.writers import (
    WriterWithTargetFormat,
    ArticleWithPricesTableHTML,
    ArticleWithPricesTableMD,
    FULL_INFO_MD,
    PREFIXES_MD,
)

from components.precios_claros.delta_writer import DeltaWriter



Comparison = Tuple[PointOfSale, ArticleWithPrices, ArticleWithPrices]


class ReportDeltaError(Exception):
    pass


class DeltaReportSample:
    def __init__(self) -> None:
        pass

    def get_categories(self, home: Path, identifier: str) -> Generator[str, None, None]:
        container = get_container(home, identifier)
        for root, dirs, files in walk(container):
            for category in dirs:
                yield category

    def next_comparison(
        self,
        home: Path,
        reference_collector: SampleCollector,
        current_collector: SampleCollector,
    ) -> Generator[Comparison, None, None]:
        for ref_place, ref_awp_table, ref_pos in reference_collector.sample_items(home):
            cur_awp_table = current_collector.get_article_with_prices_table(
                home, ref_place
            )
            yield ref_place, ref_awp_table, cur_awp_table

    def execute(
        self,
        target_home: Path,
        build_writer: Callable[[Path, str], DeltaWriter],
        reference_collector: SampleCollector,
        current_collector: SampleCollector,
    ) -> None:
        for ref_place, ref_awp_table, cur_awp_table in self.next_comparison(
            target_home, reference_collector, current_collector
        ):
            writer = build_writer(target_home, ref_place)
            writer.start()
            writer.header(
                reference_collector.sample, 
                current_collector.sample)
            for ref_awp in ref_awp_table.all_of_them():
                cur_awp = cur_awp_table.article_with_prices.get(
                    ref_awp.article.code, None
                )
                if cur_awp:
                    writer.line(ref_awp, cur_awp)
            # print(f"{ref_awp.article.code:s} - {ref_awp.article.name:s} {ref_awp.article.brand:s}")
            # print(f"   {str(ref_ps[0]):s} - {str(ref_ps[1]):s} - {str(ref_ps[2]):s}")
            # print(f"   {str(cur_ps[0]):s} - {str(cur_ps[1]):s} - {str(cur_ps[2]):s}")
            writer.footer()
            writer.stop()


# from openpyxl import Workbook
# 
# # Create a workbook and sheet
# wb = Workbook()
# ws = wb.active
# 
# # Data to be written
# data = [
#     (1, 2, 0),
#     (3, 4, 0),
#     (5, 1, 0),
#     (7, 8, 0),
#     (9, 6, 0),
# ]
# 
# # Set column widths
# ws.column_dimensions["A"].width = 15
# ws.column_dimensions["B"].width = 15
# ws.column_dimensions["C"].width = 15
# 
# # Write data to the sheet
# for row, item in enumerate(data, start=2):
#     for col, value in enumerate(item, start=1):
#         cell = ws.cell(row=row, column=col)
#         cell.value = value
#         if col == 2 and value > ws.cell(row=row, column=col-1).value:
#             cell.font = cell.font.copy(color="FF0000")
# 
# # Save the workbook
# wb.save("data.xlsx")
# 
# print("Excel file generated successfully!")
# 
