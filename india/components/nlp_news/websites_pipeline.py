import logging

from components.core import create_treestore_driver
from components.nlp import GetTextFacadeSampleTask, GetTokensSampleTask

from components.nlp_news.app import create_app
from components.nlp_news.websites import get_websites
from components.nlp_news.website_adnsur import ADNSURGetTextSampleTask


def filename():
    return __file__[:-3]


def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", filename()) as app:
        get_text_task = GetTextFacadeSampleTask("GetTextSampleTask")        
        get_text_task.add(ADNSURGetTextSampleTask())
        
        websites = get_websites()
        for identifier in websites.keys():        
            print(f"  {identifier:s}")
            with create_treestore_driver(app.fs.news, identifier) as driver:
                driver.pipeline.add(get_text_task)
                driver.pipeline.add(GetTokensSampleTask("GetTokensSampleTask"))
                driver.process_samples(True)
                driver.pipeline.remove("GetTextSampleTask")
                driver.pipeline.remove("GetTokensSampleTask")
    
if __name__ == "__main__":
    main()
