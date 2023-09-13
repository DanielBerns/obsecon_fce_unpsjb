from contextlib import contextmanager
import requests
import json
import logging

from typing import Dict, Generator, Tuple, Any, List
from precios_claros_app import PreciosClarosException


def classname(thing: Any) -> str:
    return thing.__class__.__name__

indentation = '    '


class WebScraper:
    def __init__(self) -> None:
        self._remote_home = 'https://d3e6htiiul5ek9.cloudfront.net/dev/'
        self._points_of_sale_url = self.remote_home + 'sucursales'
        self._points_of_sale_first_query_url = self.points_of_sale_url + '?limit=0'

    @property
    def remote_home(self) -> str:
        return self._remote_home

    @property
    def points_of_sale_url(self) -> str:
        return self._points_of_sale_url

    @property
    def points_of_sale_first_query_url(self) -> str:
        return self._points_of_sale_first_query_url

    def start(self) -> None:
        logging.info(f"{classname(self):s} start")
    
    def stop(self) -> None:
        logging.info(f"{classname(self):s} stop")


    def points_of_sale_page(self, page: str, queries_per_page: int) -> str:
        return self.points_of_sale_url + \
               '?offset=' + \
               str((page - 1) * queries_per_page) + \
               '&limit=' + str(queries_per_page)

    def articles_url(self, point_of_sale: str) -> str:
        return self.remote_home + 'productos?id_sucursal=' + point_of_sale

    def articles_first_query_url(self, this_articles_url: str) -> str:
        return this_articles_url + '&limit=0'

    def articles_page(self, this_articles_url: str, page: int, queries_per_page: int) -> str:
        return f"{this_articles_url:s}&offset={(page - 1) * queries_per_page:d}&limit={queries_per_page:d}"

    def get_info(self, url: str) -> Dict[any, any]:
        logging.info(f'url: {url:s}')
        try:
            response = requests.get(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0'}
            )
        except Exception as message:
            logging.debug(str(message))
            explanation = { 'origin': f'{classname(self):s}.get_info 1',
                            'error': str(message),
                            'url': url}
            raise PreciosClarosException(explanation)
        else:
            logging.info(f'{indentation:s}status_code: {response.status_code:d}')
            if response.status_code == 200:
                return response.json()
            else:
                explanation = {'origin': f'{classname(self):s}.get_info 2',
                               'error': 'unexpected status_code', 
                               'url': url,
                               'status_code': str(response.status_code)}
                raise PreciosClarosException(explanation)

    def _get_query_limits(self, info: Dict[any, any]) -> Tuple[int, int, int]:
        total = info.get('total', 0)        
        queries_per_page = info.get('maxLimitPermitido', 0)
        logging.info(f'total {str(total):s} queries_per_page {str(queries_per_page):s}')
        if total > 0 and queries_per_page > 0:
            max_number_of_pages = total // queries_per_page
        else:
            max_number_of_pages = 0
        return max_number_of_pages, total, queries_per_page

    def get_query_limits(self, url: str) -> Tuple[int, int, int]:
        info = self.get_info(url)
        error_message = info.get('error_message', None)
        if error_message:
            logging.debug(str(error_message))
            return 0, 0, 0
        else:
            return self._get_query_limits(info)

    def points_of_sale(self) -> Generator[Dict[str, str], None, None]:
        logging.info(f'{classname(self):s}.points_of_sale start')
        max_number_of_pages, total, queries_per_page = self.get_query_limits(
            self.points_of_sale_first_query_url)
        for page in range(1, max_number_of_pages + 1):
            this_url = self.points_of_sale_page(page, queries_per_page)
            info = self.get_info(this_url)
            error_message = info.get('error_message', None)
            if error_message:
                logging.error(f'{classname(self):s}.points_of_sale 2 page {page:d} -{str(error_message):s}')
                continue
            points_of_sale = info.get('sucursales', None)
            if points_of_sale:
                for a_point_of_sale in points_of_sale:
                    yield a_point_of_sale
            #else:                        
                logging.error(f'{classname(self):s}.points_of_sale 3: page {page:d} - {str(info):s}')
                # don't break
        logging.info(f'{classname(self):s}.points_of_sale done')

    def get_article_list(self,
                         articles_url: str,
                         page: int,
                         queries_per_page: int) -> List:
        this_url = self.articles_page(articles_url, page, queries_per_page)
        info = self.get_info(this_url)
        error_message = info.get('error_message', None)
        if error_message:
            logging.warning(f'{classname(self):s}.get_article_list: {page:d} - {str(error_message):s}')
            logging.warning(f'{str(info):s}')
            return None
        articles_list = info.get('productos', None)
        return articles_list

    def articles_per_point_of_sale(self, point_of_sale: Dict[str, str]) -> Generator[Dict[str, str], None, None]:
        identifier = point_of_sale['identifier']
        print(f'{classname(self):s}.articles_per_point_of_sale start: {identifier:s}')
        articles_url = self.articles_url(identifier)
        print(f"articles_url: {articles_url:s}")     
        logging.info(f"articles_url: {articles_url:s}")        
        articles_first_query_url = self.articles_first_query_url(articles_url)
        max_number_of_pages, total, queries_per_page = self.get_query_limits(articles_first_query_url)
        logging.info(f"max_number_of_pages: {max_number_of_pages:d}")
        logging.info(f"total: {total:d}")
        logging.info(f"queries_per_page: {queries_per_page:d}")        
        for page in range(1, max_number_of_pages + 1):
            articles_list = self.get_article_list(articles_url, page, queries_per_page)
            if articles_list:
                for an_article in articles_list:
                    an_article['point_of_sale'] = identifier
                    yield an_article
            else:
                logging.info("empty article_list")                        
        print(f'{classname(self):s}.articles_per_point_of_sale done {identifier:s}')


@contextmanager
def create_webscraper():
    resource = WebScraper()
    try:
        resource.start()
        yield resource
    except RuntimeError as message:
        print(message)
    finally:
        resource.stop()
