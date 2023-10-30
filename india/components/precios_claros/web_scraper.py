from contextlib import contextmanager
import requests
import json
import logging
from dataclasses import dataclass, field

from typing import Dict, Generator, Tuple, Any, List

from components.helpers import classname, i, get_timestamp

# import pdb

class WebScraperException(Exception):
    pass

@dataclass
class QueryLimits:
    total_items: int
    max_queries_per_page: int
    full_pages: int = field(init=False)
    full_page_queries: int = field(init=False)
    last_page_queries: int = field(init=False)

    def __post_init__(self) -> None:
        if self.total_items > 0 and self.max_queries_per_page > 0:
            self.full_pages: int = self.total_items // self.max_queries_per_page
            self.full_page_queries: int = self.max_queries_per_page
            self.last_page_queries: int = self.total_items % self.max_queries_per_page
        else:
            self.full_pages = self.full_page_queries = self.last_page_queries = 0

    def offset(self, page: int) -> int:
        return page * self.full_page_queries
        
        
class WebScraper:
    def __init__(self) -> None:
        self._home = 'https://d3e6htiiul5ek9.cloudfront.net/dev/'
        self._points_of_sale_url = self.home + 'sucursales'
        self._points_of_sale_first_query_url = self.points_of_sale_url + '?limit=0'

    @property
    def run_identifier(self) -> str:
        return get_timestamp()
    
    @property
    def home(self) -> str:
        return self._home

    @property
    def points_of_sale_url(self) -> str:
        return self._points_of_sale_url

    def points_of_sale_first_query_url(self) -> str:
        return self._points_of_sale_first_query_url

    def articles_first_query_url(self, this_articles_url: str) -> str:
        return this_articles_url + '&limit=0'

    def start(self) -> None:
        logging.info(f"{classname(self):s} start")
    
    def stop(self) -> None:
        logging.info(f"{classname(self):s} stop")

    def build_url(self, url: str, offset: int, queries: int) -> str:
        return f"{url:s}?offset={offset:d}&limit={queries:d}"
    
    def points_of_sale_next_query_url(self, offset: int, queries: int) -> str:
        return self.build_url(self.points_of_sale_url, offset, queries)

    def articles_per_point_of_sale_url(self, point_of_sale: str) -> str:
        return self.home + 'productos?id_sucursal=' + point_of_sale

    def articles_next_query_url(
        self, 
        this_articles_url: str, 
        offset: int, 
        queries: int) -> str:
        return f"{this_articles_url:s}&offset={offset:d}&limit={queries:d}"

    def get_info(self, url: str) -> Dict[Any, Any]:
        logging.info(f'url: {url:s}')
        try:
            response = requests.get(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
            )
        except Exception as message:
            logging.debug(str(message))
            explanation = { 'origin': f'{classname(self):s}.get_info 1',
                            'errorMessage': str(message),
                            'url': url}
            # raise WebScraperException(explanation)
            return explanation
        else:
            logging.info(f'{i(1):s}status_code: {response.status_code:d}')
            if response.status_code == 200:
                return response.json()
            else:
                explanation = {'origin': f'{classname(self):s}.get_info 2',
                               'errorMessage': 'unexpected status_code', 
                               'url': url,
                               'status_code': str(response.status_code)}
                # raise WebScraperException(explanation)
                return explanation

    def get_query_limits(self, url: str) -> QueryLimits:
        info = self.get_info(url)
        error_message = info.get('errorMessage', None)
        if error_message:
            logging.debug(str(error_message))
            total_items = max_queries_per_page = 0
        else:
            total_items = info.get('total', 0)        
            max_queries_per_page = info.get('maxLimitPermitido', 0)
        logging.info(f'total {str(total_items):s} max_queries_per_page {max_queries_per_page:d}')
        return QueryLimits(total_items, max_queries_per_page)

    def _points_of_sale(self, offset: int, queries: int) -> Generator[Dict[str, str], None, None]:
        this_url = self.points_of_sale_next_query_url(offset, queries)
        logging.info(f'{this_url:s} - offset: {offset:d} - queries: {queries:d}')
        info = self.get_info(this_url)
        error_message = info.get('errorMessage', None)
        if error_message:
            logging.warning(f'{classname(self):s}.points_of_sale 2: '\
                            f'page {offset:d} - {str(error_message):s}')
        else:
            points_of_sale = info.get('sucursales', None)
            if points_of_sale:
                for a_point_of_sale in points_of_sale:
                    yield a_point_of_sale
            else:                        
                logging.warning(f'{classname(self):s}.points_of_sale 3: '\
                                f'offset {offset:d} - {str(info):s}')
                # don't break
            
    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f'{classname(self):s}.points_of_sale 1: start')
        query_limits = self.get_query_limits(self.points_of_sale_first_query_url())
        if query_limits.total_items > 0:
            for page in range(0, query_limits.full_pages):
                for pos in self._points_of_sale(
                                query_limits.offset(page), 
                                query_limits.full_page_queries):
                    yield pos
            for pos in self._points_of_sale(
                            query_limits.offset(query_limits.full_pages), 
                            query_limits.last_page_queries):
                yield pos
        else:
            logging.info(f'{classname(self):s}.points_of_sale 2: zero query_limits')            
        logging.info(f'{classname(self):s}.points_of_sale 3: done')

    def selected_points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f'{classname(self):s}.selected_points_of_sale 1: start')
        yield from []
        logging.info(f'{classname(self):s}.selected_points_of_sale 2: done')        

    def get_article_list(self,
                         articles_url: str,
                         offset: int,
                         queries: int
                         ) -> List[Dict[str, str]]:
        logging.info(f'{classname(self):s}.get_article_list 1: start')
        this_url = self.articles_next_query_url(articles_url, offset, queries)
        logging.info(f'{i(1):s}{this_url:s} - '\
                     f'offset: {offset:d} - queries: {queries:d}')
        info = self.get_info(this_url)
        error_message = info.get('errorMessage', None)
        if error_message:
            logging.warning(f'{classname(self):s}.get_article_list 2: '\
                            f'{str(error_message):s}')
            articles_list = []
        else:
            logging.info(f'{classname(self):s}.get_article_list 3: done')            
            articles_list = info.get('productos', [])
        return articles_list

    def _articles_per_point_of_sale(self, 
                                    articles_url: str, 
                                    offset: int, 
                                    queries: int,
                                    identifier: str) -> Generator[Dict[str, str], None, None]:
        articles_list = self.get_article_list(articles_url, offset, queries)
        if articles_list:
            for number, an_article in enumerate(articles_list):
                an_article['point_of_sale'] = identifier
                logging.info(f'{classname(self):s}.articles_per_point_of_sale 3: '
                             f'{identifier:s}: {number:d}')
                yield an_article
        else:
           logging.info(f'{classname(self):s}.articles_per_point_of_sale 4: '
                        f'{identifier:s}')
           logging.info(f"{i(1):s}empty article_list")                        

    def articles_per_point_of_sale(self, 
                                   point_of_sale: Dict[str, str]
                                   ) -> Generator[Dict[str, str], None, None]:
        identifier = point_of_sale['identifier']
        articles_url = self.articles_per_point_of_sale_url(identifier)
        articles_first_query_url = self.articles_first_query_url(articles_url)
        query_limits = self.get_query_limits(articles_first_query_url)
        if query_limits.total_items > 0:
            for page in range(0, query_limits.full_pages):
                for article in self._articles_per_point_of_sale(
                                 articles_url, 
                                 query_limits.offset(page), 
                                 query_limits.full_page_queries,
                                 identifier):
                    yield article
            for article in self._articles_per_point_of_sale(
                             articles_url, 
                             query_limits.offset(query_limits.full_pages), 
                             query_limits.last_page_queries,
                             identifier):
                yield article
        else:
            logging.info(f'{classname(self):s}.articles_per_point_of_sale 2: zero query_limits')            
        logging.info(f'{classname(self):s}.articles_per_point_of_sale 3: done {identifier:s}')


@contextmanager
def create_web_scraper():
    resource = WebScraper()
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(message)
    finally:
        resource.stop()
