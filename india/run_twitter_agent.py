import logging

from app.engine import create_app
from components.twitter_agent import run

IDENTIFIER = "run_twitter_agent"

def main():
    with create_app(IDENTIFIER) as app:
        run(app.fs.twitter, app.config.authorization_token["twitter"])
    
if __name__ == '__main__':
    main()
