from contextlib import contextmanager
import logging
from pathlib import Path
from typing import TextIO, Protocol, Tuple, List, Generator, Optional
from jinja2 import Template

from components.precios_claros.models import (Article, 
                                              PointOfSale, 
                                              ArticleWithPricesTable, 
                                              PointsOfSaleTable, 
                                              PreciosClarosTask)
from components.helpers import get_container, get_resource, i, classname

def filename() -> str:
    return __file__[:-3]

class WriterError(Exception):
    pass

class TargetFormat(Protocol):
    
    @property
    def selectors(self) -> bool:
        return False
    
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
                points_of_sale: List[PointOfSale]
                ) -> None:
        if self.target_format is None:
            raise WriterError(f"classname(self).execute: target_format is None")
        container = get_container(Path(self.home, 'article_with_prices'), category)
        if article_with_prices.place != place:
            logging.debug("article_with_prices.place != place")
            logging.debug(f"  article_with_prices.place {article_with_prices.place:s}")
            logging.debug(f"  place {place:s}")    
            raise WriterError(f"{classname(self):s} bad place 1")
        if self.target_format.selectors:
            article_with_prices.load_selectors(category)
        parts = (place).split(':')
        city = self.get_city(parts[1])
        timestamp = (article_with_prices.timestamp)[:8]
        year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:]
        if category == "acba":
            title = f"Artículos de la canasta básica de alimentos en {city:s} {year:s}/{month:s}/{day:s}"
        else:
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




TABLE_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>{{ttl}}</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>

<!-- theSidebar -->
<nav class="w3-sidebar w3-bar-block w3-card w3-animate-left w3-center" style="display:none" id="theSidebar">
  <button class="w3-bar-item w3-button" onclick="closeTheSidebar()">Cerrar <i class="fa fa-remove"></i></button>
  <a href="/info/lacteos/{{this_city}}"             class="w3-bar-item w3-button w3-padding"> Lácteos</a>  
  <a href="/info/harinas/{{this_city}}"             class="w3-bar-item w3-button w3-padding"> Harinas</a>  
  <a href="/info/vegetales/{{this_city}}"           class="w3-bar-item w3-button w3-padding"> Vegetales</a>  
  <a href="/info/carnes/{{this_city}}"              class="w3-bar-item w3-button w3-padding"> Carnes</a>                        
  <a href="/info/bebidas_con_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas con alcohol</a>  
  <a href="/info/bebidas_sin_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas sin alcohol</a>  
  <a href="/info/aseo/{{this_city}}"                class="w3-bar-item w3-button w3-padding"> Artículos de aseo personal</a>  
  <a href="/info/limpieza/{{this_city}}"                class="w3-bar-item w3-button w3-padding"> Artículos de limpieza</a>    
  <a href="/info/acba/{{this_city}}"                class="w3-bar-item w3-button w3-padding"> Artículos de la canasta básica de alimentos</a>  
  <a href="/index"                                  class="w3-bar-item w3-button w3-padding">Volver al índice</a>
</nav>

<!-- theHeader -->
<header class="w3-container w3-theme w3-padding" id="theHeader">
  <i onclick="openTheSidebar()" class="fa fa-bars w3-xlarge w3-button w3-theme"></i> 
  <div class="w3-center">
  <h2>Web de precios - Observatorio de Economía - FCE</h2>
  <h1 class="w3-xxxlarge w3-animate-bottom">{{ttl}}</h1>
  <!--
    <div class="w3-padding-32">
      <button class="w3-btn w3-xlarge w3-dark-grey w3-hover-light-grey" onclick="document.getElementById('modal01').style.display='block'" style="font-weight:900;">
      Buscar
      </button>
    </div>
  -->
  </div>
</header>

<!-- Modal -->
<div id="modal01" class="w3-modal">
    <div class="w3-modal-content w3-card-4 w3-animate-top">
      <header class="w3-container w3-theme-l1"> 
        <div onclick="document.getElementById('modal01').style.display='none'"
             class="w3-button w3-display-topright">Cerrar</div>
        <p>{{ ttl }}</p>
      </header>
      <footer class="w3-container w3-theme-l1">
        <p><i class="fa fa-smile-o"></i></p>
      </footer>
    </div>
</div>

<div class="w3-card w3-container" style="min-height:460px">
<br>
<div>
<input id="searchinput" class="w3-input" oninput="filterHTML('#search', 'article', this.value)" placeholder="Buscar">
</div>
<br>
<div class="w3-container" id="search">
    {% for article in awpt.values() %}
    <article class="w3-row">
        <div class="w3-twothird w3-pale-blue">            
            <p class="w3-tooltip w3-left">
            {{article.label()}}.&nbsp;
            <span class="w3-text w3-theme-light w3-padding">
               <a href="#theHeader"><i class="fa fa-chevron-up">&nbsp;</i></a>
            </span>
            </p>
        </div>
        <div class="w3-third w3-pale-green">
            <p class="w3-tooltip w3-right">
            <i class="fa fa-usd"></i>{{article.prices_geomean()}}            
            <span class="w3-text">{{article.prices_range()}}&nbsp;</span>
            </p>
        </div>
    </article>
    {% endfor %}
</div>
</div>

<footer class="w3-container w3-theme">
  <p class="w3-opacity">Hecho por Gipis - DIE - FI - UNPSJB</p>
</footer>


<script>
// Side navigation
function openTheSidebar() {
  var x = document.getElementById("theSidebar");
  x.style.width = "100%";
  // x.style.fontSize = "20px";
  x.style.paddingTop = "10%";
  x.style.display = "block";
}
function closeTheSidebar() {
  document.getElementById("theSidebar").style.display = "none";
}
function getElements(id) {
  if (typeof id == "object") {
    return [id];
  } else {
    return document.querySelectorAll(id);
  }
}
function filterHTML(id, sel, filter) {
  var a, b, c, i, ii, iii, hit;
  a = getElements(id);
  for (i = 0; i < a.length; i++) {
    b = a[i].querySelectorAll(sel);
    for (ii = 0; ii < b.length; ii++) {
      hit = 0;
      if (b[ii].innerText.toUpperCase().indexOf(filter.toUpperCase()) > -1) {
        hit = 1;
      }
      c = b[ii].getElementsByTagName("*");
      for (iii = 0; iii < c.length; iii++) {
        if (c[iii].innerText.toUpperCase().indexOf(filter.toUpperCase()) > -1) {
          hit = 1;
        }
      }
      if (hit == 1) {
        b[ii].style.display = "";
      } else {
        b[ii].style.display = "none";
      }
    }
  }
}
</script>


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



FULL_INFO_MD = """
# Código ~ artículo ~ indicativo ~ mínimo ~ máximo
{% for aa in awpt.all_of_them() %} {{aa.label()}} | {{aa.prices_geomean()}} | {{aa.prices_min()}} | {{aa.prices_max()}} 
{% endfor %}
"""

PREFIXES_MD = """
{% for aa in awpt.all_of_them() %} {{aa.article.name}}
{% endfor %}
"""

class ArticleWithPricesTableMD:
    def __init__(self, 
                 text: str,
                 selectors: bool = False,
                 ) -> None:
        self._selectors: bool = selectors
        self._text: str = text
        
    @property
    def selectors(self) -> bool:
        return self._selectors

    @property
    def text(self) -> str:
        return self._text
    
    @property
    def template(self) -> Template:
        return Template(self._text)
               
    @property
    def suffix(self) -> str:
        return ".csv"
