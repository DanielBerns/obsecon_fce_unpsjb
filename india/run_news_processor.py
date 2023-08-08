# run_news_processor

from application import create_app, get_websites
from components.website_agent import processor_run
from application import ADNSUR

IDENTIFIER = "run_news_processor"

def main() -> None:
    websites = get_websites()
    with create_app(IDENTIFIER) as app:
       processor_run(app.fs.news, app.fs.results, websites)

    # websites = {}
    # websites["adnsur"] = [
    #     ("https://adnsur.com.ar", ADNSUR())]
    # processor_run("/home/dberns/Data/observatorio-economico/",
    #               "/home/dberns/Data/observatorio-economico/results", websites)
    
if __name__ == "__main__":
    main()
