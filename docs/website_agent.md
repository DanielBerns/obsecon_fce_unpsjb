in website_bot.py
        
    class WebsiteBot(Bot):
    
    def run_website_bot_fn(
        bot_home: Path, 
        identifier: str, 
        url: str) -> None:

in website_processor.py

    class WebsiteProcessor:
        def execute(self, identifier: str):
        
in adnsur_extractor.py

    class ADNSURExtractor(FileProcessor):
        ## HTML -> Text
        
in adnsur_nlp.py

    class ADNSURNLP(WebsiteProcessor):
