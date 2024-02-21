from typing import Callable, Dict
from components.core import Application, FlatStore, show
from components.configuration import CLI
from components.helpers import get_container, get_timestamp
from components.precios_claros.io import IO, Sample

import pdb

class Actions:
    @staticmethod
    def create_sample(
        application: Application, select: Callable[[Dict[str, str]], bool]
    ) -> str:
        precios_claros = get_container(
            application.file_system.storage, "precios_claros"
        )
        store = FlatStore(precios_claros, "flatstore")
        store.start()
        timestamp = get_timestamp()
        sample_home = store.sample_home(timestamp)
        sample = IO.build(timestamp, sample_home)
        sample.start()
        IO.write(sample, select)
        sample.stop()
        store.stop()
        return sample.key

    @staticmethod
    def report_sample(
        application: Application, sample_key: str, report_key: str
    ) -> None:
        precios_claros = get_container(
            application.file_system.storage, "precios_claros"
        )
        store = FlatStore(precios_claros, "flatstore")
        store.start()
        sample_home = store.sample_home(sample_key)
        sample = IO.build(sample_key, sample_home)
        show(f"sample_key: {sample_key:s}")
        points_of_sale_table, articles_reader = IO.read(sample)
        for key, value in articles_reader.articles_counter.items():
            print(f"{key:<60s}: {value:d}")
        print(len(articles_reader.articles_counter))
        showit = False
        if showit:
            for place, article_with_prices_table, points_of_sale_table in IO.iterate(
                sample, 
                points_of_sale_table, 
                articles_reader
            ):
                print(f"place: {place:s}")
                for article_with_prices in article_with_prices_table.values():
                    print(f"  {article_with_prices.article.name:s}")
        store.stop()

    @staticmethod
    def report_sample_delta(
        application: Application, reference: Sample, current: Sample, report_key: str
    ) -> None:
        pass
