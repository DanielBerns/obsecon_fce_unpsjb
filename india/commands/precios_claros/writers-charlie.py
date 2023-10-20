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
        title = f"{category:s} en {city:s} - {year:s}/{month:s}/{day:s}"        
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
<div class="w3-bar w3-teal" style="z-index:4">
  <button class="w3-bar-item w3-button w3-hide-large w3-hover-none w3-hover-text-light-green" onclick="w3_open();"><i class="fa fa-bars"></i>  Menu</button>
  <div class="w3-bar-item w3-hide-small"><img src="/static/img/chakana.svg" width="50"></div>                    
  <h1 class="w3-bar-item w3-right">Observatorio de precios - FCE - UNPSJB</h1>
</div>

<!-- Sidebar/menu -->
<nav class="w3-sidebar w3-collapse w3-white w3-animate-left" style="z-index:3;width:300px;" id="mySidebar"><br>
  <div class="w3-bar-block">
    <a href="#" class="w3-bar-item w3-button w3-padding-16 w3-hide-large w3-dark-grey w3-hover-black" onclick="w3_close()" title="cerrar menu"><i class="fa fa-remove fa-fw"></i>  Cerrar menú</a>
    <a href="/info/lacteos/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Lácteos</a>
    <a href="/info/harinas/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Harinas</a>
    <a href="/info/vegetales/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Vegetales</a>
    <a href="/info/carnes/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Carnes</a>                      
    <a href="/info/bebidas_con_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas con alcohol</a>
    <a href="/info/bebidas_sin_alcohol/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Bebidas sin alcohol</a>
    <a href="/info/acba/{{this_city}}" class="w3-bar-item w3-button w3-padding"> Artículos de la canasta básica de alimentos</a>
    <a href="/index" class="w3-bar-item w3-button w3-padding">Volver al índice</a>    
    <div class="w3-bar-item">
        <div class="w3-container w3-right">
          <button onclick="document.getElementById('id01').style.display='block'" 
                  class="w3-button w3-pale-green">¿Precio indicativo?</button>
          <div id="id01" class="w3-modal">
            <div class="w3-modal-content">
              <div class="w3-container">
                <span onclick="document.getElementById('id01').style.display='none'" class="w3-button w3-display-topright">&times;</span>
                <p>El precio indicativo es el promedio geométrico de los precios observados.</p>
                <p>Si todos los precios observados son iguales, solo se muestre el precio indicativo.</p>
              </div>
            </div>
          </div>
        </div>
    </div>
  </div>
</nav>

<!-- Overlay effect when opening sidebar on small screens -->
<div class="w3-overlay w3-hide-large w3-animate-opacity" 
     onclick="w3_close()" 
     style="cursor:pointer" 
     title="Cerrar menú lateral" id="myOverlay">
</div>

<!-- Header -->

<!-- Main content container -->   
<div class="w3-main" style="margin-left:300px;margin-top:10px;">
<div class="w3-bar-block">
   <div class="w3-bar-item">
     <header class="w3-sand">
       <h2 class="w3-center w3-padding-8">Precios {{ ttl }}</h2>
     </header>
   </div>
   <div class="w3-bar-item">
     <div class="w3-row">
        <div class="w3-twothird">
           <input class="w3-input w3-border w3-padding" 
                  type="text" 
                  placeholder="Buscar..." 
                  id="searchInput" 
                  onkeyup="searchArticleTable()">
        </div>
        <div class="w3-third">
        </div>
     </div>
   </div>
   <div class="w3-bar-item">
     <div class="tableFixedHeader">
       <table class="w3-table w3-striped w3-border-black w3-hoverable w3-white" 
              id="articleTable" >
       <thead class="w3-sand">
       <tr>
         <th class="w3-center">
         <p>Artículo</p></th>
         <th class="w3-center"><p>Precio indicativo</p></th>
         <th class="w3-center"><p>Precio mínimo</p></th>
         <th class="w3-center"><p>Precio máximo</p></th>
       </tr>
       </thead>
       <tbody>
            {% for article in awpt.values() %}
            <tr>                      
            <td>{{article.label()}}</td>
            <td class="w3-right-align">{{article.prices_geomean(10)}}</td>
            <td class="w3-right-align">{{article.prices_min(10)}}</td>            
            <td class="w3-right-align">{{article.prices_max(10)}}</td>
             </tr>
            {% endfor %}
       </tbody>
       </table><br>
     </div> <!-- End of tableFixedHeader -->
   </div>
</div> <!-- End bar block -->
</div> <!-- End w3-main -->

<!-- Footer -->
<footer class="w3-container w3-sand w3-right-align w3-bottom w3-hide-small">
  <p>Hecho por GIPIS - DIE - FI - UNPSJB</p>
</footer>

<script src="/static/js/table.js"></script>   
</body>
</html>
"""

class ArticleWithPricesTableHTML:
    def __init__(self):
        pass
    
    @property
    def template(self) -> Template:
        return Template(TABLE_HTML)
               
    @property
    def suffix(self) -> str:
        return ".html"


TABLE_MD = """
# {{ ttl }} 

## Artículo: mínimo - indicativo - máximo &&
{% for aa in awpt.all_of_them() %} 
    {{aa.label()}}: {{aa.prices_stats[1]}} {% if aa.prices_stats[0] != aa.prices_stats[2] %} [[ {{aa.prices_stats[0]}} -- {{aa.prices_stats[2]}} ]] {% endif %}
    {% for pos, pp, fpp in aa.formatted_prices %}{{pos}}: {{fpp}}
    {% endfor %}
{% endfor %}
"""

class ArticleWithPricesTableMD:
    def __init__(self):
        pass
    
    @property
    def template(self) -> Template:
        return Template(TABLE_MD)
               
    @property
    def suffix(self) -> str:
        return ".md"
