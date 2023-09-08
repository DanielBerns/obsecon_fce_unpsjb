import logging

from application import create_app
from news import get_websites
from adnsur import ADNSURGetTextSampleTask

from context import components
from components.core import create_treestore_driver
from components.nlp import GetTextFacadeSampleTask, GetTokensSampleTask

NAME = "run_news_pipeline"

def main() -> None:
    with create_app("observatorio_fce_unpsjb", "india", "test", NAME) as app:
        print("app created!")
        get_text_task = GetTextFacadeSampleTask("GetTextSampleTask")        
        get_text_task.add(ADNSURGetTextSampleTask())
       
        for identifier, urls in get_text_task.sources():        
            print(f"  {identifier:s}")
            with create_treestore_driver(app.fs.news, identifier) as driver:
                driver.pipeline.add(get_text_task)
                driver.pipeline.add(GetTokensSampleTask("GetTokensSampleTask"))
                driver.process_samples(True)
                driver.pipeline.remove("GetTextSampleTask")
                driver.pipeline.remove("GetTokensSampleTask")
    
if __name__ == "__main__":
    main()
