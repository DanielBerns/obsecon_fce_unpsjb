# run_news_processor

from components.helpers import get_command
from application import create_app, get_websites
from components.website_agent import processor_run
from application import ADNSURExtractor

IDENTIFIER = "run_news_processor"

RUN = get_command("RUN")

def main() -> None:
    websites = get_websites()
    with create_app(IDENTIFIER) as app:
       processor_run(app.fs.news, app.fs.results, websites)
    
if __name__ == "__main__":
    main()
