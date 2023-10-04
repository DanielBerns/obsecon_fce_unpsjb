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
        self._suffix = resource.suffix

    @property
    def resource(self) -> Path:
        return self._resource

    @property
    def template(self) -> Template:
        with open(self.resource, 'r') as source:
            return Template(source.read())        

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
        article_with_prices.load_selectors(category)
        parts = (place).split(':')
        city = self.get_city(parts[1])
        timestamp = (article_with_prices.timestamp)[:8]
        year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:]
        title = f"{city:s} - {year:s}/{month:s}/{day:s}"        
        template = self.target_format.template
        page = template.render(
            awpt=article_with_prices, 
            pos=points_of_sale, 
            ttl=title)
        city_in_filename = parts[1].replace(' ', '_')
    
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
<html lang="es">
<head>
<title>{{ ttl }}</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">               
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
<link href="/static/img/favicon.ico" rel="shortcut icon">
<link rel="stylesheet" href="/static/css/table.css">
</head>
<body class="w3-pale-green">

<!-- Top container -->
<div class="w3-bar w3-top w3-teal w3-large" style="z-index:4">
  <button class="w3-bar-item w3-button w3-hide-large w3-hover-none w3-hover-text-light-green" onclick="w3_open();"><i class="fa fa-bars"></i>  Menu</button>
  <div class="w3-bar-item w3-left">
  <img src="/static/img/chakana.svg" width="50">  
  </div>                    
  <span class="w3-bar-item w3-right">Observatorio de precios - FCE - UNPSJB</span>
</div>

<!-- Sidebar/menu -->
<nav class="w3-sidebar w3-collapse w3-white w3-animate-left" style="z-index:3;width:300px;" id="mySidebar"><br>
  <hr>
  <div class="w3-container">
    <h5>Tipos de productos</h5>
  </div>
  <div class="w3-bar-block">
    <a href="#" class="w3-bar-item w3-button w3-padding-16 w3-hide-large w3-dark-grey w3-hover-black" onclick="w3_close()" title="close menu"><i class="fa fa-remove fa-fw"></i>  Cerrar menú</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Harinas</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Lácteos</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Frutas y vegetales</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Aceite</a>                      
    <a href="#" class="w3-bar-item w3-button w3-padding"> Bebidas alcohólicas</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Gaseosas y agua de mesa</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Conservas</a>
    <a href="#" class="w3-bar-item w3-button w3-padding"> Otros</a>                      
    <a href="#" class="w3-bar-item w3-button w3-padding"> Otros</a><br><br>
  </div>
</nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large w3-animate-opacity" 
     onclick="w3_close()" 
     style="cursor:pointer" 
     title="Cerrar menú lateral" id="myOverlay">
</div>

<!-- Main content container -->   
<div class="w3-main" style="margin-left:300px;margin-top:43px;">
   
   <!-- Header -->
   <header class="w3-container w3-sand" style="padding-top:22px">
     <p class="w3-center"><b>Precios {{ ttl }}</b></p>
   </header>
   <div class="w3-container">
   <!-- Search -->
     <p>Búsqueda de artículos</p>
     <input class="w3-input w3-border w3-padding" 
            type="text" 
            placeholder="Buscar..." 
            id="searchInput" 
            onkeyup="searchArticleTable()">
     <hr>
     <div class="tableFixedHeader">
       <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white" 
              id="articleTable" >
       <thead class="w3-sand">
       <tr>
         <th class="w3-center">Artículo</th>
         <th class="w3-center">Precio mínimo</th>
         <th class="w3-center">Precio indicativo</th>
         <th class="w3-center">Precio máximo</th>
       </tr>
       </thead>
       <tbody>
            {% for article in awpt.values() %}
            <tr>                      
            <td>{{article.label()}}</td>
            <td class="w3-right-align">{{article.prices_min(10)}}</td>
            <td class="w3-right-align">{{article.prices_geomean(10)}}</td>
            <td class="w3-right-align">{{article.prices_max(10)}}</td>
             </tr>
            {% endfor %}
       </tbody>
       </table><br>
     </div> <!-- End of tableFixedHeader -->
   </div> <!-- End of unnamed w3-container -->
   <hr>
  
   </div>    <!-- End w3-main -->

      <!-- Footer -->
   <footer class="w3-container w3-sand w3-right-align w3-bottom">
     <p>Hecho por GIPIS - DIE - FI - UNPSJB</p>
   </footer>

   <script src="/static/js/table.js"></script>   
</body>
</html>
"""

class ArticleWithPricesTableTargetFormat:
    def __init__(self):
        pass
    
    @property
    def template(self) -> Template:
        return Template(TABLE_HTML)
               
    @property
    def suffix(self) -> str:
        return ".html"
