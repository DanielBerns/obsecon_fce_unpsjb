import logging

from application import create_app, get_websites, ADNSURGetTextSampleTask

from components.core import create_treestore_driver
from components.nlp import GetTextFacadeSampleTask, GetTokensSampleTask

def main() -> None:
    with create_app("run_news_pipeline") as app:
        print("app created!")
        get_text_task = GetTextFacadeSampleTask("GetTextSampleTask")        
        get_text_task.add(ADNSURGetTextSampleTask())
       
        for key, urls in get_text_task.sources():        
            print(f"  {key:s}")
            with create_treestore_driver(app.fs.news, key) as driver:
                driver.pipeline.add(get_text_task)
                driver.pipeline.add(GetTokensSampleTask("GetTokensSampleTask"))
                driver.process_samples(True)
                driver.pipeline.remove("GetTextSampleTask")
                driver.pipeline.remove("GetTokensSampleTask")

    
if __name__ == "__main__":
    main()
