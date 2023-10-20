from contextlib import contextmanager
import logging
from pathlib import Path
from typing import TextIO, Protocol, Tuple, List, Generator
from models import Article, PointOfSale, Writer
from components.helpers import get_container, get_resource

import pdb

def filename() -> str:
    return __file__[:-3]

HTML_START = """
<!DOCTYPE html>
<html>
<head>

<title>Precios</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
<link href="/static/img/favicon.ico" rel="shortcut icon">
</head>
<body>

<header class="w3-container w3-theme w3-padding" id="myHeader">
  <img src="./static/img/chakana.svg" width="100" height="100" onclick="w3_open()">  
  <div class="w3-center">
  <h1 class="w3-xxxlarge">Observatorio de precios - FCE - UNPSJB</h4>
  <h4 class="w3-animate-bottom">El sur de la información</h1>
  </div>
</header>
"""

HTML_STOP = """
<!-- Footer -->
<footer class="w3-container w3-theme-dark w3-padding-16">
  
  <div style="position:relative;bottom:55px;" class="w3-tooltip w3-right">
    <span class="w3-text w3-theme-light w3-padding">Ir arriba</span>    
    <a class="w3-text-white" href="#myHeader"><span class="w3-xlarge">
    <i class="fa fa-chevron-circle-up"></i></span></a>
  </div>
</footer>

</body>
</html>

"""

TABLE_ARTICLES_START = """
<table class="w3-table w3-striped w3-bordered">
<thead>
<tr class="w3-theme">
  <th>Artículo</th>  
  <th>Precio mínimo</th>
  <th>Precio indicativo</th>
  <th>Precio máximo</th>
</tr>
</thead>
<tbody>
"""

TABLE_POINTS_OF_SALE_START = """
<table class="w3-table w3-striped w3-bordered">
<thead>
<tr class="w3-theme">
  <th>Precio</th>
  <th>Identificador</th>
  <th>Nombre</th>
  <th>Dirección</th>
</tr>
</thead>
<tbody>
"""
TABLE_STOP = """
</tbody>
</table>
"""

class HTMLWriter:
    def __init__(self, target: TextIO, place: str) -> None:
        self._target = target
        self._place = place

    @property
    def target(self) -> TextIO:
        return self._target
    
    def start(self) -> None:
        self.target.write(HTML_START)
    
    def stop(self) -> None:
        self.target.write(HTML_STOP)

    def place(self) -> str:
        return self._place
    
    def header(self) -> None:
        self.target.write(f"<h1>Precios en {self.place:s}</h1>")
 
    def article(self, 
                article_code: str, 
                this_article: Article, 
                prices_stats: Tuple[str, str, str],
                formatted_prices_list: List[Tuple[PointOfSale, str]]
                ) -> None:
        self.target.write('<div class="w3-container">\n')
        self.target.write('<div class="w3-card">\n')        
        self.target.write(TABLE_ARTICLES_START)
        self.target.write("<tr>\n")
        self.target.write(f"<td>{article_code:s}: {this_article.brand:s} - {this_article.name:s}</td>")                
        self.target.write(f"<td>{prices_stats[0]:>9s}</td>")        
        self.target.write(f"<td>{prices_stats[1]:>9s}</td>")
        self.target.write(f"<td>{prices_stats[2]:>9s}</td>")
        self.target.write("</tr>\n\n")
        self.target.write(TABLE_STOP)
        self.target.write("\n\n")
        # self.target.write(TABLE_POINTS_OF_SALE_START)
        # for point_of_sale, price in formatted_prices_list:
        #     self.target.write("<tr>\n")                            
        #     self.target.write(f"<td>{price:>9s}</td>")
        #     self.target.write(f"<td>{point_of_sale.identifier:>20s}</td>")
        #     self.target.write(f"<td>{point_of_sale.name}</td>")
        #     self.target.write(f"<td>{point_of_sale.address}</td>")
        #     self.target.write("</tr>\n\n")
        # self.target.write(TABLE_STOP)
        self.target.write("</div>")        
        self.target.write("</div>")


@contextmanager    
def html_writer(sample_container: Path, place: str) -> Generator[Writer, None, None]:
    place_container = get_container(sample_container, place)
    point_of_sale_and_price_per_code_html = get_resource(
        place_container, f'{place:s}_precios', '.html')
    with open(point_of_sale_and_price_per_code_html, 'w') as target:
        writer = HTMLWriter(target, place)
        writer.start()        
        try:
            yield writer
        except Exception as message:
            logging.warning(f"{filename():s}.html_writer: {str(message):s}")
        finally:
            writer.stop()



class MarkdownWriter:
    def __init__(self, target: TextIO, place: str) -> None:
        self._target = target
        self._place = place

    @property
    def target(self) -> TextIO:
        return self._target

    def place(self) -> str:
        return self.place
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass
    
    def header(self) -> None:            
        self.target.write(f"# {self.place:s}\n")
 
    def article(self, 
                article_code: str, 
                this_article: Article, 
                prices_stats: Tuple[str, str, str],
                formatted_prices_list: Generator[Tuple[PointOfSale, str], None, None]
                ) -> None:
        pdb.set_trace()
        self.target.write(f"## {article_code:s}: ")
        self.target.write(f"{this_article.brand:s} -")
        self.target.write(f" {this_article.name:s} -")
        self.target.write(f" {this_article.package:s}\n")
        for point_of_sale, price in formatted_prices_list:
            self.target.write(f"{i(1):s}{price:>9s} - "
                              f"{point_of_sale.identifier:>20s} - "
                              f"{point_of_sale.name} - "
                              f"{point_of_sale.city} - "
                              f"{point_of_sale.address}\n" )
       
@contextmanager    
def markdown_writer(sample_container: Path, place: str) -> Generator[Writer, None, None]:
    place_container = get_container(sample_container, place)
    point_of_sale_and_price_per_code_md = get_resource(
        place_container, f'{place:s}_precios', '.md')
    with open(point_of_sale_and_price_per_code_md, 'w') as target:
        writer = MarkdownWriter(target, place)
        writer.start()        
        try:
            yield writer
        except Exception as message:
            logging.warning(f"{filename():s}.markdown_writer: {str(message):s}")
        finally:
            writer.stop()
        
