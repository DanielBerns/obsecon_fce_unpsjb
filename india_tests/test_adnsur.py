from pathlib import Path

from application import ADNSURGetText
from components.nlp import NLPGetTokens
from components.website_agent import Website, run_website_pipeline

ADNSUR_PIPELINE = [ADNSURGetText(), NLPGetTokens()]

def main():
    base = Path('~', 'Data', 'observatorio-economico').expanduser()
    websites = [Website("adnsur", "https://adnsur.com.ar", ADNSUR_PIPELINE),
                ]
    run_website_pipeline(base, websites)
    
if __name__ == "__main__":
    main()
