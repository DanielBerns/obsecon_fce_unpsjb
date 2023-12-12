from components.telegram_agent import run_bot
from components.nlp_news import create_app


run_bot(secrets_home, info_home, bot_identifier)
