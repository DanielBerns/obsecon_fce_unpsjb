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
    def content(self) -> str:
        return ""
    
    def suffix(self) -> str:
        return ""

    
class FromFileTargetFormat:    
    def __init__(self, resource: Path) -> None:
        with open(resource, 'r') as source:
            self._content = source.read()
        self._suffix = resource.suffix

    @property
    def content(self) -> str:
        return self._content

    @property
    def suffix(self) -> str:
        return ".txt"


class HTMLTargetFormat:
    def __init__(self):
        pass
    
    @property
    def content(self) -> str:
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
        
        container = get_container(self.home, 'articles_with_prices')
        if article_with_prices.place != place:
            logging.debug("article_with_prices.place != place")
            logging.debug(f"  article_with_prices.place {article_with_prices.place:s}")
            logging.debug(f"  place {place:s}")    
            raise PreciosClarosTaskException(f"{classname(self):s} bad place 1")
        parts = (place).split(':')
        city = (parts[1]).replace(' ', '_')
        timestamp = (article_with_prices.timestamp)[:8]
        title = f"{parts[0]:s} {parts[1]:s} {timestamp:s}"
        template = Template(self.target_format.content)
        page = template.render(awpt=article_with_prices, pos=points_of_sale, title=title)
        articles_with_prices_file = get_resource(container, city, self.target_format.suffix)        
        with open(articles_with_prices_file, 'w') as target:
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

