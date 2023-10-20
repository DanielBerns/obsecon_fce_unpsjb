from contextlib import contextmanager
import logging
from pathlib import Path
from typing import TextIO, Protocol, Tuple, List, Generator, Optional
from jinja2 import Template

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
    def template(self) -> str:
        return ""

    @property    
    def suffix(self) -> str:
        return ""

    
class FromFileTargetFormat:    
    def __init__(self, resource: Path) -> None:
        with open(resource, 'r') as source:
            self._template = source.read()
        self._suffix = resource.suffix

    @property
    def template(self) -> str:
        return self._template

    @property
    def suffix(self) -> str:
        return ".txt"


class HTMLTargetFormat:
    def __init__(self):
        pass
    
    @property
    def template(self) -> str:
        return """
               <!DOCTYPE html>
               <html>
               <head>
               
               <title>{{ title }}</title>
               <meta charset="UTF-8">
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
               <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">
               <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
               <link href="/static/img/favicon.ico" rel="shortcut icon">
               <style>
                   /* width */        
                   ::-webkit-scrollbar {
                       width: 10px;
                   }
           
                   /* Track */
                   ::-webkit-scrollbar-track {
                       background: #f1f1f1;
                   }
           
                   /* Handle */
                   ::-webkit-scrollbar-thumb {
                       background: #050505;
                   }
           
                   /* Handle on hover */
                   ::-webkit-scrollbar-thumb:hover {
                       background: #a7ed91;
                   }
                   
                   .scroll {
                       display: block;
                       border: 1px solid green;
                       background: #18bbcf;
                       padding: 5px;
                       margin-top: 5px;
                       margin-bottom: 5px;                       
                       width: auto;
                       height: 400px;
                       overflow-y: scroll;
                   }
               </style>
               </head>
               <body>
               
               <header class="w3-container w3-theme w3-padding" id="myHeader">
               <div class="w3-row">
                 <div class="w3-col m1">
                 <img src="/static/img/chakana.svg" width="50">  
                 </div>
                 <div class="w3-rest w3-center">
                     <h1 class="w3-xxxlarge">Observatorio de precios - FCE - UNPSJB</h1>
                     <h4 class="w3-animate-bottom">El sur de la información</h4>
                 </div>
               </div>
               </header>
               
               <div class="w3-container">
                     <div class="w3-row w3-pale-green" width="98%">
                        <div class="w3-col m6 w3-center">Artículo</div>
                        <div class="w3-col m2 w3-right-align">Precio mínimo</div>
                        <div class="w3-col m2 w3-right-align">Precio indicativo</div>
                        <div class="w3-col m2 w3-right-align">Precio máximo</div>
                     </div>
                     <div class="w3-container scroll">
                           {% for article in awpt.values() %}
                             <div class="w3-row w3-pale-green">
                               <div class="w3-col m6 w3-left-align">{{article.label()}}</div>
                               <div class="w3-col m2 w3-right-align">{{article.prices_min(10)}}</div>
                               <div class="w3-col m2 w3-right-align">{{article.prices_geomean(10)}}</div>
                               <div class="w3-col m2 w3-right-align">{{article.prices_max(10)}}</div>
                             </div>
                           {% endfor %}
                     </div>
               </div>
               <div class="w3-row">
               </div>
               <footer class="w3-container w3-theme w3-padding-16">
               <h3 class="w3-center">Observatorio de precios - FCE - UNPSJB</h3>
               </footer>
               </body>
               </html>
               """
               
    @property
    def suffix(self) -> str:
        return ".html"
              







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

    def execute(self, 
                place: str,
                article_with_prices: ArticleWithPricesTable,
                points_of_sale: PointsOfSaleTable
                ) -> None:
        
        container = get_container(self.home, 'article_with_prices')
        if article_with_prices.place != place:
            logging.debug("article_with_prices.place != place")
            logging.debug(f"  article_with_prices.place {article_with_prices.place:s}")
            logging.debug(f"  place {place:s}")    
            raise PreciosClarosTaskException(f"{classname(self):s} bad place 1")
        parts = (place).split(':')
        city = (parts[1]).replace(' ', '_')
        timestamp = (article_with_prices.timestamp)[:8]
        year, month, day = timestamp[:4], timestamp[4:6], timestamp[6:]
        title = f"{parts[0]:s} {parts[1]:s} {timestamp:s}"
        header_title = f"{city.capitalize():s} - {year:s}/{month:s}/{day:s}"
        template = Template(self.target_format.template)
        page = template.render(awpt=article_with_prices, 
                               pos=points_of_sale, 
                               title=title,
                               header_title=header_title)
        article_with_prices_file = get_resource(container, city, self.target_format.suffix)        
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


class NewTargetFormat:
    def __init__(self):
        pass
    
    @property
    def template(self) -> str:
        return """
               <!DOCTYPE html>
               <html>
               <head>
               
               <title>{{ title }}</title>
               <meta charset="UTF-8">
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
               <link rel="stylesheet" href="https://www.w3schools.com/lib/w3-theme-teal.css">
               <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">               
               <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.3.0/css/font-awesome.min.css">
               <link href="/static/img/favicon.ico" rel="shortcut icon">
                  <style>
                  html,body,h1,h2,h3,h4,h5 {font-family: "Raleway", sans-serif}
                  .tableFixedHeader {
                    overflow-y: auto; /* make the table scrollable if height is more than 280px  */
                    height: 280px; /* gives an initial height of 280px to the table */
                  }
                  .tableFixedHeader thead th {
                    position: sticky; /* make the table heads sticky */
                    top: 0px; /* table head will be placed from the top of the table and sticks to it */
                  }
                  table {
                    border-collapse: collapse; /* make the table borders collapse to each other */
                    width: 100%;
                  }
                  th,
                  td {
                    padding: 8px 16px;
                    border: 1px solid #aaa;
                  }
                  th {
                    background: #eee;
                  }
                  </style>
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
                  <div class="w3-overlay w3-hide-large w3-animate-opacity" onclick="w3_close()" style="cursor:pointer" title="close side menu" id="myOverlay"></div>
                  
                  <div class="w3-main" style="margin-left:300px;margin-top:43px;">
                  
                    <!-- Header -->
                    <header class="w3-container w3-light-grey" style="padding-top:22px">
                      <p class="w3-center"><b>Precios {{ header_title }}</b></p>
                    </header>
                    <div class="w3-container">
                      <p>Búsqueda de artículos</p>
                      <input class="w3-input w3-border w3-padding" 
                             type="text" placeholder="Buscar..." id="searchInput" onkeyup="searchArticleTable()">
                      <hr>
                      <div class="tableFixedHeader">
                        <table class="w3-table w3-striped w3-bordered w3-border w3-hoverable w3-white" id="articleTable" >
                        <thead class="w3-pale-green">
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
                      </div>
                    </div>
                    <hr>
                  
                    <!-- Footer -->
                    <footer class="w3-container w3-light-grey w3-right-align w3-bottom">
                      <p>Hecho por GIPIS - DIE - FI - UNPSJB</p>
                    </footer>
                  
                    <!-- End page content -->
                  </div>
                  
                  <script>
                  // Get the Sidebar
                  var mySidebar = document.getElementById("mySidebar");
                  
                  // Get the DIV with overlay effect
                  var overlayBg = document.getElementById("myOverlay");
                  
                  // Toggle between showing and hiding the sidebar, and add overlay effect
                  function w3_open() {
                    if (mySidebar.style.display === 'block') {
                      mySidebar.style.display = 'none';
                      overlayBg.style.display = "none";
                    } else {
                      mySidebar.style.display = 'block';
                      overlayBg.style.display = "block";
                    }
                  }
                  
                  // Close the sidebar with the close button
                  function w3_close() {
                    mySidebar.style.display = "none";
                    overlayBg.style.display = "none";
                  }
                  
                  function searchArticleTable() {
                    var input, filter, table, tr, td, i;
                    input = document.getElementById("searchInput");
                    filter = input.value.toUpperCase();
                    table = document.getElementById("articleTable");
                    tr = table.getElementsByTagName("tr");
                    for (i = 0; i < tr.length; i++) {
                      td = tr[i].getElementsByTagName("td")[0];
                      if (td) {
                        txtValue = td.textContent || td.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                          tr[i].style.display = "";
                        } else {
                          tr[i].style.display = "none";
                        }
                      }
                    }
                  }
                  </script>
                  
                  </body>
                  </html>
               """
               
    @property
    def suffix(self) -> str:
        return ".html"
