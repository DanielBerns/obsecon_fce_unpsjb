from contextlib import contextmanager
import logging
from pathlib import Path
from typing import TextIO, Protocol, Tuple, List, Generator, Optional
from jinja2 import Template

import pdb

from models import (Article, 
                    PointOfSale, 
                    ArticleWithPricesTable, 
                    PointsOfSaleTable, 
                    PreciosClarosTask,
                    PreciosClarosTaskException)
from context import components
from components.helpers import get_container, get_resource, i, classname

def filename() -> str:
    return __file__[:-3]



class TargetFormat(Protocol):
    @property    
    def template(self) -> Template:
        return Template("")

    @property    
    def suffix(self) -> str:
        return ""

    
class FromFileTargetFormat:    
    def __init__(self, resource: Path) -> None:
        self._resource = resource

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def template(self) -> Template:
        with open(self.resource, 'r') as origin:
            return Template(origin.read())        

    @property
    def suffix(self) -> str:
        return self.resource.suffix


class WriterWithTargetFormat:
    def __init__(self, home: Path) -> None:
        self._home = home
        self._target_format: Optional[TargetFormat] = None
        
    @property
    def home(self) -> Path:
        return self._home
    
    @property
    def target_format(self) -> Optional[TargetFormat]:
        return self._target_format
    
    @target_format.setter
    def target_format(self, value: TargetFormat) -> None:
        self._target_format = value
    
    def start(self) -> None:
        pass
    
    def stop(self) -> None:
        pass

    def get_city(self, text: str) -> str:
        parts = text.split(' ')
        return ' '.join([pp.capitalize() for pp in parts])

    def execute(self, 
                place: str,
                category: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: PointsOfSaleTable
                ) -> None:
        
        container = get_container(Path(self.home, 'article_with_prices'), category)
        if article_with_prices.place != place:
            logging.debug("article_with_prices.place != place")
            logging.debug(f"  article_with_prices.place {article_with_prices.place:s}")
            logging.debug(f"  place {place:s}")    
            raise PreciosClarosTaskException(f"{classname(self):s} bad place 1")
        if self.target_format.selectors:
            article_with_prices.load_selectors(category)
        parts = (place).split(':')
        city = self.get_city(parts[1])
        timestamp = (article_with_prices.timestamp)[:8]
        year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:]
        title = f"{category.replace('_',' '):s} en {city:s} - {year:s}/{month:s}/{day:s}"        
        city_in_filename = parts[1].replace(' ', '_')
        template = self.target_format.template
        page = template.render(
            awpt=article_with_prices, 
            pos=points_of_sale, 
            ttl=title,
            this_city=city_in_filename)
        article_with_prices_file = get_resource(
            container, city_in_filename, self.target_format.suffix)        
        with open(article_with_prices_file, 'w') as target:
            target.write(page)


@contextmanager    
def writer_with_target_format(container: Path) -> Generator[PreciosClarosTask, None, None]:
    writer = WriterWithTargetFormat(container)
    writer.start()        
    try:
        yield writer
    except Exception as message:
        logging.warning(f"{filename():s}.{classname(writer):s}: {str(message):s}")
    finally:
        writer.stop()


TABLE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
<link href="/static/img/favicon.ico" rel="shortcut icon">
<link rel="stylesheet" href="/static/css/table.css">
</head>
<body>

<div class="top-container w3-light-blue">
  <div class="w3-bar w3-teal" style="z-index:4">
    <div class="w3-bar-item w3-left"><img src="/static/img/chakana.svg" width="50px"></div>                    
    <h1 class="w3-bar-item w3-right w3-hide-small">Web de Precios - Observatorio de Economía - FCE
    </h1>
    <h1 class="w3-bar-item w3-right w3-hide-medium w3-hide-large">Web de Precios
    </h1>
    <div class="w3-bar-item">
        <h2 class="w3-center w3-padding-8">Precios {{ ttl }}</h2>
    </div>
  </div>
</div>

<!-- Sidebar -->
<div class="w3-display-container">
<div class="w3-sidebar w3-border-right w3-display-topleft" style="display:none" id="mySidebar">
<div class="w3-bar-block">
  <button onclick="w3_close('mySidebar')" class="w3-bar-item w3-large">Cerrar &times;</button>
  <a href="/info/lacteos/{{this_city}}"             class="w3-bar-item w3-button w3-padding"> Lácteos</a>  
  <a href="/info/harinas/{{this_city}}"             class="w3-bar-item w3-button w3-padding"> Harinas</a>  
  <a href="/info/vegetales/{{this_city}}"           class="w3-bar-item w3-button w3-padding"> Vegetales</a>  
  <a href="/info/carnes/{{this_city}}"              class="w3-bar-item w3-button w3-padding"> Carnes</a>                        
  <a href="/info/bebidas_con_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas con alcohol</a>  
  <a href="/info/bebidas_sin_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas sin alcohol</a>  
  <a href="/info/acba/{{this_city}}"                class="w3-bar-item w3-button w3-padding"> Artículos de la canasta básica de alimentos</a>  
  <a href="/index"                                  class="w3-bar-item w3-button w3-padding">Volver al índice</a>
</div>
</div>
</div>

<div class="header w3-pale-green w3-text-black" id="myHeader">
    <div class="w3-row-padding">
      <div class="w3-col w3-left l2 m2 s2">
        <button class="w3-button w3-hover-none" onclick="w3_open('mySidebar');"><i class="fa fa-bars"></i></button>
      </div>
      <div class="w3-col l10 m10 s10">
         <input class="w3-input w3-border w3-padding" 
                type="text" 
                placeholder="Buscar..." 
                id="searchInput" 
                onkeyup="searchArticleTable()">
      </div>
    </div>
    <div class="w3-row-padding">
      <div class="w3-col w3-left l10 m10 s10">
        <p>Artículo</p>
      </div>
      <div class="w3-col w3-left l2 m2 s2">
        <p class="w3-tooltip">Precio de referencia 
        <span class="w3-text">. El precio de referencia es el promedio geométrico de los precios observados.</span></p>
      </div>  
    </div>
</div>

<div class="content w3-light-gray" id="articleTable">
  <div class="w3-container">
  <table class="w3-table w3-bordered w3-hoverable">
      {% for article in awpt.values() %}
      <tr class="row">      
          <td>
            <p class="searchThis w3-tooltip">
            {{article.label()}}.&nbsp;<span class="w3-text">{{article.prices_range()}}</span>
            </p>
          </td>
          <td>
            <p>
            <span class="w3-right">{{article.prices_geomean()}}</span>
            </p>
          </td>
      </tr>
      {% endfor %}
  </table>
  </div>
</div>
<script src="/static/js/table.js"></script>
</body>
</html>
"""

class ArticleWithPricesTableHTML:
    def __init__(self, selectors: bool = True) -> None:
        self._selectors: bool = selectors
        
    @property
    def selectors(self) -> bool:
        return self._selectors
    
    @property
    def template(self) -> Template:
        return Template(TABLE_HTML)
               
    @property
    def suffix(self) -> str:
        return ".html"


# TABLE_MD = """
# # {{ ttl }} 
# 
# ## Artículo: mínimo - indicativo - mínimo - máximo
# {% for aa in awpt.all_of_them() %} 
#     {{aa.label()}}: {{aa.prices_geomean()}} - {{aa.prices_min()}} - {{aa.prices_max()}}
#     {% for pos, pp, fpp in aa.formatted_prices %}{{pos}}: ${{fpp}}
#     {% endfor %}
# {% endfor %}
# """

TABLE_MD = """
# Código - artículo - indicativo - mínimo - máximo
{% for aa in awpt.all_of_them() %} {{aa.label()}} - {{aa.prices_geomean()}} - {{aa.prices_min()}} - {{aa.prices_max()}} 
{% endfor %}
"""

class ArticleWithPricesTableMD:
    def __init__(self, selectors: bool = False) -> None:
        self._selectors: bool = selectors
        
    @property
    def selectors(self) -> bool:
        return self._selectors
    
    @property
    def template(self) -> Template:
        return Template(TABLE_MD)
               
    @property
    def suffix(self) -> str:
        return ".csv"
